from django.conf.urls import patterns, include, url

urlpatterns = patterns('todo.views',
    
    url(r'^login/?$', 'login_view', name='todo_login'),
    url(r'^register/?$', 'register', name='todo_register'),
    url(r'^logout/?$', 'logout_view', name='todo_logout'),
    url(r'^list/?$', 'todo_list', name='todo_list'),
    url(r'^add/?$', 'add_todo', name='todo_add'),
    url(r'^edit/?$', 'view_edit', name='todo_edit'),
    )
