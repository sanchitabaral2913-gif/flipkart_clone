from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.conf import settings
from django.templatetags.static import static



# Add new student
def student_add(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student:list')
    else:
        form = StudentForm()
    return render(request, 'student/student_form.html', {'form': form, 'student': None})

# Edit student
def student_edit(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student:list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student/student_form.html', {'form': form, 'student': student})

# Delete student
def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        student.delete()
        return redirect('student:list')
    return render(request, 'student/student_delete.html', {'student': student})

# student_list view
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student/student_list.html', {'students': students})

