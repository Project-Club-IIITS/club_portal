from django.shortcuts import render
from .models import Calendar
import datetime
import calendar
from .forms import CalendarForm, ChooseMonthAndYearForm

# from first_app.forms import calendar_data
# Create your views here.
next_m = 0
next_y = 0
back_m = 0
back_y = 0


def currentdate():
    return datetime.date.today()


# def index(request):
#     return render(request, 'put_calendar/index.html')


def hello(request, select, show):
    x = currentdate()
    y = x.isoformat()
    year = int(y[:4])
    month = int(y[5:7])

    global next_m
    next_m = month
    global next_y
    next_y = year
    global back_m
    back_m = month
    global back_y
    back_y = year

    mandy = ChooseMonthAndYearForm()

    if select != '1':

        trig = select.split('m')


        year = int(trig[0])
        month = int(trig[1])

        if int(show) < 10:
            sdate = '0' + str(show)

        else:
            sdate = str(show)

        if int(month) < 10:
            smonth = '0' + str(month)

        else:
            smonth = str(month)

        final_date = str(year) + '-' + str(smonth) + '-' + str(sdate)

        if request.method == 'POST':
            form = CalendarForm(request.POST)

            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.user = request.user
                form_instance.date = final_date
                form_instance.save()

                form = CalendarForm()

            month_calendar = calendar.monthcalendar(year, month)

            month_name = calendar.month_name[month]
            year_name = str(month_name + ' , ' + str(year))
            len_month = len(month_calendar)

            p = []
            b = []

            for i in range(len(month_calendar)):
                for j in range(len(month_calendar[i])):
                    if month_calendar[i][j] > 0:
                        if month_calendar[i][j] < 10:
                            y = str('0' + str(month_calendar[i][j]))
                            p.append(y)
                        if month_calendar[i][j] >= 10:
                            y = str(month_calendar[i][j])
                            p.append(y)

            q = []
            for i in range(len(p)):
                if month < 10:
                    c = str(str(year) + '-0' + str(month) + '-' + p[i])
                else:
                    c = str(str(year) + '-' + str(month) + '-' + p[i])
                q.append(c)

            dates_with_works = []
            work_on_date = []
            for i in range(len_month):
                a = [0, 0, 0, 0, 0, 0, 0]
                b.append(a)

            dates_needed = []

            query = Calendar.objects.filter(user=request.user, date=final_date).order_by('date')

            for i in range(len(query)):
                s = str(query[i].work_title)
                work_on_date.append(s)
                c = query[i].date
                d = c.isoformat()
                dates_needed.append(d)
                dates_with_works.append(int(d[8:10]))

            for m in range(len(q)):
                for i in range(len(b)):
                    for j in range(len(b[i])):
                        for k in range(len(dates_with_works)):
                            if month_calendar[i][j] == dates_with_works[k] and q[m] == dates_needed[k]:
                                b[i][j] = [dates_with_works[k], work_on_date[k]]

            print(b)
            return render(request, 'accounts/put_templates/date.html',
                          {'year_no': str(year) + 'm' + str(month), 'month_cal': month_calendar,
                           'zipped_data': zip(month_calendar, b), 'present_year': year_name, 'form': form,
                           'final_date': final_date, 'events': query, 'mandy': mandy})

        else:
            form = CalendarForm()

            month_calendar = calendar.monthcalendar(year, month)

            month_name = calendar.month_name[month]
            year_name = str(month_name + ' , ' + str(year))
            len_month = len(month_calendar)

            p = []
            b = []

            for i in range(len(month_calendar)):
                for j in range(len(month_calendar[i])):
                    if month_calendar[i][j] > 0:
                        if month_calendar[i][j] < 10:
                            y = str('0' + str(month_calendar[i][j]))
                            p.append(y)
                        if month_calendar[i][j] >= 10:
                            y = str(month_calendar[i][j])
                            p.append(y)

            q = []
            for i in range(len(p)):
                if month < 10:
                    c = str(str(year) + '-0' + str(month) + '-' + p[i])
                else:
                    c = str(str(year) + '-' + str(month) + '-' + p[i])
                q.append(c)

            dates_with_works = []
            work_on_date = []
            for i in range(len_month):
                a = [0, 0, 0, 0, 0, 0, 0]
                b.append(a)

            dates_needed = []

            query = Calendar.objects.filter(user=request.user, date=final_date).order_by('date')

            for i in range(len(query)):
                s = str(query[i].work_title)
                work_on_date.append(s)
                c = query[i].date
                d = c.isoformat()
                dates_needed.append(d)
                dates_with_works.append(int(d[8:10]))

            for m in range(len(q)):
                for i in range(len(b)):
                    for j in range(len(b[i])):
                        for k in range(len(dates_with_works)):
                            if month_calendar[i][j] == dates_with_works[k] and q[m] == dates_needed[k]:
                                b[i][j] = [dates_with_works[k], work_on_date[k]]

            print(b)
            return render(request, 'accounts/put_templates/date.html',
                          {'year_no': str(year) + 'm' + str(month), 'month_cal': month_calendar,
                           'zipped_data': zip(month_calendar, b), 'present_year': year_name, 'form': form,
                           'final_date': final_date, 'events': query, 'mandy': mandy})

    else:

        month_calendar = calendar.monthcalendar(year, month)

        month_name = calendar.month_name[month]
        year_name = str(month_name + ' , ' + str(year))
        len_month = len(month_calendar)

        p = []
        b = []

        for i in range(len(month_calendar)):
            for j in range(len(month_calendar[i])):
                if month_calendar[i][j] > 0:
                    if month_calendar[i][j] < 10:
                        y = str('0' + str(month_calendar[i][j]))
                        p.append(y)
                    if month_calendar[i][j] >= 10:
                        y = str(month_calendar[i][j])
                        p.append(y)

        q = []
        for i in range(len(p)):
            if month < 10:
                c = str(str(year) + '-0' + str(month) + '-' + p[i])
            else:
                c = str(str(year) + '-' + str(month) + '-' + p[i])
            q.append(c)

        dates_with_works = []
        work_on_date = []
        for i in range(len_month):
            a = [0, 0, 0, 0, 0, 0, 0]
            b.append(a)

        dates_needed = []

        query = Calendar.objects.order_by('work_title')

        for i in range(len(query)):
            s = str(query[i].work_title)
            work_on_date.append(s)
            c = query[i].date
            d = c.isoformat()
            dates_needed.append(d)
            dates_with_works.append(int(d[8:10]))

        for m in range(len(q)):
            for i in range(len(b)):
                for j in range(len(b[i])):
                    for k in range(len(dates_with_works)):
                        if month_calendar[i][j] == dates_with_works[k] and q[m] == dates_needed[k]:
                            b[i][j] = [dates_with_works[k], work_on_date[k]]
        print(b)
        return render(request, 'accounts/put_templates/date.html',
                      {'year_no': str(year) + 'm' + str(month), 'month_cal': month_calendar,
                       'zipped_data': zip(month_calendar, b), 'present_year': year_name, 'mandy': mandy})


def date(request, select, show):
    global back_m
    global back_y
    global next_m
    global next_y
    if next_m < 12 and next_m >= 1:
        next_m = next_m + 1
        next_y = next_y
    else:
        next_m = 1
        next_y = next_y + 1
    back_m = next_m
    back_y = next_y
    return grid(request, next_y, next_m)


def date1(request, select, show):
    global back_m
    global back_y
    global next_m
    global next_y
    if back_m > 1 and back_m <= 12:
        back_m = back_m - 1
        back_y = back_y
    else:
        back_m = 12
        back_y = back_y - 1
    next_m = back_m
    next_y = back_y
    return grid(request, back_y, back_m)


def choose_event(request, select, show):
    if request.method == 'POST':
        form = ChooseMonthAndYearForm(request.POST)

        month = int(request.POST['month'])
        year = int(request.POST['year'])

        return grid(request, year, month)


def grid(request, year, month):
    mandy = ChooseMonthAndYearForm()

    if request.method == 'POST':
        form = CalendarForm(request.POST)

        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = request.user
            form_instance.save()

        month_calendar = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        year_name = str(month_name + ' , ' + str(year))

        len_month = len(month_calendar)

        b = []
        dates_with_works = []
        dates_needed = []
        p = []
        for i in range(len(month_calendar)):
            for j in range(len(month_calendar[i])):
                if month_calendar[i][j] > 0:
                    if month_calendar[i][j] < 10:
                        y = str('0' + str(month_calendar[i][j]))
                        p.append(y)
                    if month_calendar[i][j] >= 10:
                        y = str(month_calendar[i][j])
                        p.append(y)

        q = []
        work_on_date = []
        for i in range(len(p)):
            if month < 10:
                c = str(str(year) + '-0' + str(month) + '-' + p[i])
            else:
                c = str(str(year) + '-' + str(month) + '-' + p[i])
            q.append(c)

        for i in range(len_month):
            a = [0, 0, 0, 0, 0, 0, 0]
            b.append(a)

        query = Calendar.objects.all()

        for i in range(len(query)):
            s = str(query[i].work_title)
            work_on_date.append(s)
            c = query[i].date
            d = c.isoformat()
            dates_needed.append(d)
            dates_with_works.append(int(d[8:10]))


        for m in range(len(q)):
            for i in range(len(b)):
                for j in range(len(b[i])):
                    for k in range(len(dates_with_works)):
                        if month_calendar[i][j] == dates_with_works[k] and q[m] == dates_needed[k]:
                            b[i][j] = [dates_with_works[k], work_on_date[k]]

        return render(request, 'accounts/put_templates/date.html',
                      {'year_no': str(year) + 'm' + str(month), 'month_cal': month_calendar,
                       'zipped_data': zip(month_calendar, b), 'present_year': year_name, 'mandy': mandy})

    else:
        form = CalendarForm()

        month_calendar = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        year_name = str(month_name + ' , ' + str(year))

        len_month = len(month_calendar)

        b = []
        dates_with_works = []
        dates_needed = []
        p = []
        for i in range(len(month_calendar)):
            for j in range(len(month_calendar[i])):
                if month_calendar[i][j] > 0:
                    if month_calendar[i][j] < 10:
                        y = str('0' + str(month_calendar[i][j]))
                        p.append(y)
                    if month_calendar[i][j] >= 10:
                        y = str(month_calendar[i][j])
                        p.append(y)

        q = []
        work_on_date = []
        for i in range(len(p)):
            if month < 10:
                c = str(str(year) + '-0' + str(month) + '-' + p[i])
            else:
                c = str(str(year) + '-' + str(month) + '-' + p[i])
            q.append(c)

        for i in range(len_month):
            a = [0, 0, 0, 0, 0, 0, 0]
            b.append(a)

        query = Calendar.objects.all()

        for i in range(len(query)):
            s = str(query[i].work_title)
            work_on_date.append(s)
            c = query[i].date
            d = c.isoformat()
            dates_needed.append(d)
            dates_with_works.append(int(d[8:10]))



        for m in range(len(q)):
            for i in range(len(b)):
                for j in range(len(b[i])):
                    for k in range(len(dates_with_works)):
                        if month_calendar[i][j] == dates_with_works[k] and q[m] == dates_needed[k]:
                            b[i][j] = [dates_with_works[k], work_on_date[k]]

        return render(request, 'accounts/put_templates/date.html',
                      {'year_no': str(year) + 'm' + str(month), 'month_cal': month_calendar,
                       'zipped_data': zip(month_calendar, b), 'present_year': year_name, 'mandy': mandy})


def event_enter(request, date_selected):
    if request.method == 'POST':
        form = CalendarForm(request.POST)

        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = request.user
            form_instance.save()

    else:
        form = CalendarForm()
    return render(request, 'accounts/put_templates/date.html', {'form': form})