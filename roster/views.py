from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from .models import Employee, Availability, Shift, DutyRoster
from django.contrib.auth.decorators import login_required
from datetime import timedelta, timezone

# Create your views here.

#@login_required
def import_availability(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        # Read Excel file using pandas
        df = pd.read_excel(file, engine='openpyxl')

        for index, row in df.iterrows():
            employee_name = row['Employee Name']  # Make sure your column matches
            employee, created = Employee.objects.get_or_create(first_name=row['First Name'], last_name=row['Last Name'])
            date = row['Date']  # Ensure column name matches
            is_available = row['Availability']  # 1 = Available, 0 = Unavailable
            
            # Create the Availability record
            Availability.objects.update_or_create(
                employee=employee,
                date=date,
                defaults={'is_available': is_available}
            )
        return HttpResponse("Availability imported successfully!")
    return render(request, 'roster/import_availability.html')

from datetime import timedelta

def generate_roster_for_month(request, month, year):
    employees = Employee.objects.all()
    shifts = []
    
    # Generate a list of dates for the month
    from calendar import monthrange
    first_day, last_day = monthrange(year, month)
    
    for day in range(1, last_day + 1):
        date = timezone.datetime(year, month, day).date()
        shift = Shift.objects.create(date=date)
        shifts.append(shift)
    
    # Now, assign employees to shifts considering their availability and the 2-day gap rule
    for shift in shifts:
        available_employees = [e for e in employees if Availability.objects.filter(employee=e, date=shift.date, is_available=True).exists()]
        
        if not available_employees:
            # If no one is available, handle the case (e.g., leave empty or notify)
            continue
        
        # Assign an employee to this shift considering the 2-day gap constraint
        for employee in available_employees:
            # Find the most recent shift assigned to this employee
            recent_shift = DutyRoster.objects.filter(employee=employee).order_by('-date').first()
            if recent_shift and (shift.date - recent_shift.date).days < 2:
                continue  # Skip this employee due to the 2-day gap constraint
            
            DutyRoster.objects.create(employee=employee, shift=shift, date=shift.date)
            break  # Stop after assigning one employee to the shift
    
    return HttpResponse("Roster for the month generated successfully!")
