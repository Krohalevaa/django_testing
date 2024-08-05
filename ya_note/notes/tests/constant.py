from django.urls import reverse
# ADD_URL = reverse('notes:add')
# LIST_URL = 
# EDIT_URL = 

ADD_URl = reverse('notes:add')
cls.list_url = reverse('notes:list')
cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
