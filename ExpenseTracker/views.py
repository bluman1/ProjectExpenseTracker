import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ExpenseTracker.models import User, Expense


def validate_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def show_home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            # show user home.
            user = User.objects.get(email=request.user.email)
            full_name = user.get_first_name()
            expenses = Expense.objects.filter(created=datetime.datetime.today()).filter(user=user)
            total = 0
            for expense in expenses:
                total += expense.cost
            c = {
                'full_name': full_name,
                'date': datetime.datetime.today(),
                'total': total,
            }
            return render(request, 'base.html', c)
        else:
            # show landing page for anonymous users.
            return render(request, 'landing_page.html', {})
    elif request.method == 'POST':
        # find a workaround for creating multiple expenses simultaneously
        type_ = request.POST.get('type')
        cost = request.POST.get('cost')
        cost = float(cost)
        description = request.POST.get('description')
        user = User.objects.get(email=request.user.email)
        expense = Expense(type=type_, cost=cost, description=description, user=user)
        expense.save()
        full_name = user.get_first_name()
        expenses = Expense.objects.filter(created=datetime.datetime.today()).filter(user=user)
        total = 0
        for expense in expenses:
            total += expense.cost
        c = {
            'full_name': full_name,
            'date': datetime.datetime.today(),
            'total': total,
            'msg': '<div class="alert alert-success"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><strong>Success!</strong> Expense Created.</div>'
        }
        return render(request, 'base.html', c)


def show_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return render(request, "base_login.html")
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            """return invalid login here"""
            return render(request, 'base_login.html', {'error': '<div class="alert alert-danger"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><strong>Failed!</strong> Invalid Details</div>.'})


def show_signup(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        render(request, 'base_signup.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if not validate_email(email):
            return render(request, 'base_signup.html', {'error': '<div class="alert alert-danger"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><strong>Invalid email!</strong> Enter a valid email.</div>.'})
        if len(password) < 6:
            return render(request, 'base_signup.html', {'error': '<div class="alert alert-danger"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><strong>Password too short!</strong> Enter a password longer than that.</div>.'})
        if password != password_again:
            return render(request, 'base_signup.html', {'error': '<div class="alert alert-danger"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><strong>Password mismatch!</strong> Enter matching passwords</div>.'})
        try:
            User.objects.get(email=email)
            render(request, 'base_signup.html', {'error': '<div class="alert alert-danger"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><strong>Email already exists!</strong> Email already exists</div>.'})
        except User.DoesNotExist:
            pass
        user = User.objects.create_user(email, password, first_name, last_name)
        auth_user = authenticate(email=email, password=password)
        if user is not None:
            login(request, auth_user)
            return HttpResponseRedirect('/')
        else:
            """return invalid login here"""
            return render(request, 'base_signup.html', {'error': '<div class="alert alert-danger"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><strong>Failed to login!</strong> Please go to login page</div>.'})


@login_required
def show_expense_history(request):
    if request.method == 'GET':
        user = User.objects.get(email=request.user.email)
        full_name = user.get_first_name()
        date = datetime.datetime.today()
        try:
            expenses = Expense.objects.filter(created=date).filter(user=user).order_by('created')
            total = 0
            for expense in expenses:
                total += expense.cost
            c = {
                'expenses': expenses,
                'full_name': full_name,
                'date': date,
                'total': total
            }
            return render(request, 'base_expense_history.html', c)
        except Expense.DoesNotExist:
            c = {
                'full_name': full_name,
                'date': date,
                'msg': 'No expenses yet.'
            }
            return render(request, 'base_expense_history.html', c)
    elif request.method == 'POST':
        date = request.POST.get('date')
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        user = User.objects.get(email=request.user.email)
        full_name = user.get_first_name()
        try:
            expenses = Expense.objects.filter(created=date).filter(user=user).order_by('created')
            total = 0
            for expense in expenses:
                total += expense.cost
            c = {
                'expenses': expenses,
                'full_name': full_name,
                'date': date,
                'total': total
            }
            return render(request, 'base_expense_history.html', c)
        except Expense.DoesNotExist:
            c = {
                'full_name': full_name,
                'date': date,
                'msg': 'No expense was recorded on this date.'
            }
            return render(request, 'base_expense_history.html', c)

@login_required
def show_profile(request):
    if request.method == 'GET':
        return render(request, 'base_month_expense.html')
    elif request.method == 'POST':
        data = request.POST
        old_password = data['old_password']
        new_password = data['new_password']
        new_password_again = data['new_password_again']

        user = User.objects.get(email=request.user.email)
        if old_password is not user.password:
            c = {
                'errors': 'Your old password is incorrect'
            }
            return render(request, 'base_month_expense.html', c)
        else:
            if new_password is not new_password_again:
                c = {
                    'errors': 'Your new password does not match'
                }
                return render(request, 'base_month_expense.html', c)
            else:
                user.password = new_password
                user.save()
                c = {
                    'message': 'Password successfully changed'
                }
                return render(request, 'base_month_expense.html', c)


@login_required
def show_logout(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect('/')
