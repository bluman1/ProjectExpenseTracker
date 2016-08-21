from django.shortcuts import render_to_response


# Create your views here.


def login(request):

    return render_to_response("base_future_time.html", {"new_time": new_time, "offset": offset})


def signup(request):
    pass


def create_new_expense(request):
    pass


def view_day_expense(request):
    pass


def view_week_expense(request):
    pass


def view_month_expense(request):
    pass


def view_expense_history(request):
    pass


def view_about(request):
    pass


def view_profile(request):
    pass

