from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Course, Category
from .forms import CourseForm


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'course_detail.html', {'course': course})


@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})


@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'course_form.html', {'form': form})


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'course_confirm_delete.html', {'course': course})


def api_courses(request):
    courses = Course.objects.all()
    data = list(courses.values())
    return JsonResponse(data, safe=False)


def api_course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    data = {
        'id': course.id,
        'title': course.title,
        'instructor': course.instructor,
        'description': course.description,
        'year': course.year,
        'semester': course.semester,
        'category': course.category.name,
    }
    return JsonResponse(data)
