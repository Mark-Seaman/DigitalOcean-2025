from django.urls import path

from .views_note import JumbotronView, NoteCreateView, NoteDeleteView, NoteDetailView, NoteListView, NoteUpdateView, StacieView
from .views import BouncerRedirectView, ContactView, GalleryView, PubCoverView, PubDetailView, PubLibraryView, PubListView, PubRampView, PubRedirectView, PubView

urlpatterns = [

    path('favicon.ico', PubLibraryView.as_view()),

    # Pub Redirect
    path("", PubRedirectView.as_view()),
    path("pubs", PubLibraryView.as_view(), name="pub_list"),
    path("pubs/<str:pub_type>", PubListView.as_view(), name="pub_list"),
    path("<int:id>", BouncerRedirectView.as_view()),

    # Yearbook
    path("yearbook", GalleryView.as_view(), name="yearbook"),
    path("yearbook/<str:album>", GalleryView.as_view()),
    path("yearbook/<str:album>/<str:page>", GalleryView.as_view()),

    # Notes
    path('note/', NoteListView.as_view(), name='note_list'),
    path('note/<int:pk>', NoteDetailView.as_view(), name='note_detail'),
    path('note/<int:pk>/', NoteUpdateView.as_view(), name='note_edit'),
    path('note/add', NoteCreateView.as_view(), name='note_add'),
    path('note/<int:pk>/delete',  NoteDeleteView.as_view(), name='note_delete'),

    # Mark & Stacie
    path('marks', PubView.as_view()),
    path('stacie', StacieView.as_view()),
    path('stacie/<str:doc>', StacieView.as_view()),

    # Blog Pub Ramp
    path("<int:month>-<int:day>", PubRampView.as_view()),
    path("<int:month>-<int:day>/<str:type>", PubRampView.as_view()),

    # Pub Cover
    path("cover/<str:pub>", PubCoverView.as_view()),

    # Display a pub document
    path("<str:pub>", PubDetailView.as_view(), name="pub_detail"),
    path("<str:pub>/contact", ContactView.as_view()),
    path("<str:pub>/<str:doc>", PubView.as_view(), name="pub"),

]
