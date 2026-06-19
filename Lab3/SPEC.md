Avem un proiect Django cu o aplicatie numita 'courses'. Trebuie sa completezi implementarea pe baza arhitecturii MTV.
1. In `catalog/settings.py`: Adauga 'courses' in INSTALLED_APPS si seteaza LOGIN_REDIRECT_URL = '/' si LOGOUT_REDIRECT_URL = '/'.
2. In `courses/models.py`: Implementeaza modelele Category si Course (cu campurile title, instructor, description, year, semester, category).
3. In `courses/views.py`: Completeaza functiile CRUD: `course_list`, `course_detail`, `course_create`, `course_edit` si `course_delete`. De asemenea, creeaza view-urile pentru API: `api_courses` si `api_course_detail`.
4. In `courses/forms.py`: Creeaza `CourseForm` bazat pe modelul Course.
5. In `courses/urls.py`: Configureaza toate rutele pentru aplicatie si API. Integreaza-le in `catalog/urls.py`.
6. In `courses/templates/`: Creeaza `base.html`, `course_list.html`, `course_detail.html`, `course_form.html`, `course_confirm_delete.html` si folderul `registration/` cu `login.html`.

Asigura-te ca tot codul este functional, include importurile necesare (inclusiv login_required unde e cazul) si ruleaza fara erori.
