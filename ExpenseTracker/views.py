from django.shortcuts import render_to_response


# Create your views here.


def login(request):
    return render_to_response("base_login.html")


def signup(request):
    return render_to_response("base_signup.html")


def create_new_expense(request):
    return render_to_response("base_new_expense.html")


def view_day_expense(request):
    return render_to_response("base_day_expense.html")


def view_week_expense(request):
    return render_to_response("base_week_expense.html")


def view_month_expense(request):
    return render_to_response("base_month_expense.html")


def view_expense_history(request):
    return render_to_response("base_expense_history.html")


def view_about(request):
    pass


def view_profile(request):
    pass

