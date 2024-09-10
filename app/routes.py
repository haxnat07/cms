from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.auth.models import Product
from app.auth.forms import ProductForm
from app.extensions import db