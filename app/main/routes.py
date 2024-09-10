from flask import render_template, redirect, url_for, flash, request
from app.main import main_bp
from app.extensions import db
from app.main.models import Project,Task
from app.auth.models import User
from flask_login import login_required

@main_bp.route('/')
@login_required
def index():
    projects = Project.query.all()
    return render_template('home.html',projects=projects)


@main_bp.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        # Validate the inputs
        if not name or not description:
            flash('Name and Description are required!', 'danger')
        elif len(name) < 2 or len(name) > 100:
            flash('Project Name must be between 2 and 100 characters.', 'danger')
        elif len(description) < 10 or len(description) > 255:
            flash('Description must be between 10 and 255 characters.', 'danger')
        else:
            # Create and save the project
            project = Project(name=name, description=description)
            db.session.add(project)
            db.session.commit()
            flash('Project added successfully!', 'success')
            return redirect(url_for('main.add_project'))
    
    return render_template('add_project.html')

@main_bp.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        project.name = request.form.get('name')
        project.description = request.form.get('description')

        # Validate the inputs
        if not project.name or not project.description:
            flash('Name and Description are required!', 'danger')
        elif len(project.name) < 2 or len(project.name) > 100:
            flash('Project Name must be between 2 and 100 characters.', 'danger')
        elif len(project.description) < 10 or len(project.description) > 255:
            flash('Description must be between 10 and 255 characters.', 'danger')
        else:
            db.session.commit()
            flash('Project updated successfully!', 'success')
            return redirect(url_for('main.index', project_id=project.id))
    
    return render_template('edit_project.html', project=project)

@main_bp.route('/delete_project/<int:project_id>', methods=['GET','POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    
    return redirect(url_for('main.index'))  # Redirect to a suitable page, e.g., homepage or list of projects


@main_bp.route('/project/<int:project_id>') 
@login_required
def project_details(project_id): 

    project = Project.query.get_or_404(project_id) 

    tasks = Task.query.filter_by(project_id=project_id).all() 

    return render_template('project_details.html', project=project, tasks=tasks) 

 

@main_bp.route('/add_task/<int:project_id>', methods=['GET', 'POST'])
@login_required
def add_task(project_id):
    project = Project.query.get_or_404(project_id)
    users = User.query.all()
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        assigned_users = request.form.getlist('users')

        # Validate the inputs
        if not title or not description or not status:
            flash('Title, Description, and Status are required!', 'danger')
        elif status not in ['To Do', 'In Progress', 'Done', 'Late']:
            flash('Invalid status. Must be one of: todo, in progress, done, late.', 'danger')
        elif len(title) < 2 or len(title) > 100:
            flash('Title must be between 2 and 100 characters.', 'danger')
        elif len(description) < 10 or len(description) > 255:
            flash('Description must be between 10 and 255 characters.', 'danger')
        else:
            # Create and save the task
            task = Task(title=title, description=description, status=status, project=project)

            # Add the selected users to the task
            for user_id in assigned_users:
                user = User.query.get(user_id)
                if user:
                    task.users.append(user)
                    
            db.session.add(task)
            db.session.commit()
            flash('Task added successfully!', 'success')
            return redirect(url_for('main.project_details', project_id=project_id))
    
    return render_template('add_task.html', project=project, users=users)


# Edit Task
@main_bp.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    all_users = User.query.all()
    
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.status = request.form.get('status')
        assigned_users = request.form.getlist('users')

        # Validate the inputs
        if not task.title or not task.description or not task.status:
            flash('Title, Description, and Status are required!', 'danger')
        elif task.status not in ['To Do', 'In Progress', 'Done', 'Late']:
            flash('Invalid status. Must be one of: todo, in progress, done, late.', 'danger')
        elif len(task.title) < 2 or len(task.title) > 100:
            flash('Title must be between 2 and 100 characters.', 'danger')
        elif len(task.description) < 10 or len(task.description) > 255:
            flash('Description must be between 10 and 255 characters.', 'danger')
        else:
            # Update users associated with the task
            task.users = []
            for user_id in assigned_users:
                user = User.query.get(user_id)
                if user:
                    task.users.append(user)

            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('main.project_details', project_id=task.project_id))
    
    assigned_user_ids = [user.id for user in task.users]
    
    return render_template('edit_task.html', task=task, all_users=all_users, assigned_user_ids=assigned_user_ids)

# Delete Task
@main_bp.route('/delete_task/<int:task_id>', methods=['GET','POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    
    return redirect(url_for('main.project_details', project_id=project_id))
