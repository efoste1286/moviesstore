from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Heart
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Movie, Review, Heart, Petition, PetitionVote
from django.db.models import Count

def index(request):
    movies = Movie.objects.all()

    if request.user.is_authenticated:
        hearted_ids = set(
            Heart.objects.filter(user=request.user).values_list("movie_id", flat=True)
        )
    else:
        hearted_ids = set()

    for m in movies:
        m.ihearted = m.id in hearted_ids   

    template_data = {"movies": movies}
    return render(request, "movies/index.html", {"template_data": template_data})

def show(request, id):
    movie = get_object_or_404(Movie, pk=id)
    reviews = Review.objects.filter(movie=movie)

    if request.user.is_authenticated:
        movie.ihearted = Heart.objects.filter(user=request.user, movie=movie).exists()
    else:
        movie.ihearted = False

    template_data = {
        "movie": movie,
        "reviews": reviews,
    }
    return render(request, "movies/show.html", {"template_data": template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@require_POST
@login_required
def toggle_heart(request, id):
    movie = get_object_or_404(Movie, pk=id)
    qs = Heart.objects.filter(user=request.user, movie=movie)
    if qs.exists():
        qs.delete()                       # un-heart
    else:
        Heart.objects.create(user=request.user, movie=movie)  # heart
    return redirect(request.META.get("HTTP_REFERER", "/movies/"))

@login_required
def petitions_index(request):
    # List all petitions with current yes counts
    petitions = (
        Petition.objects
        .annotate(yes_total=Count("petitionvote"))
        .order_by("-created_at")
    )

    template_data = {
        "title": "Petitions",
        "petitions": petitions,
    }
    return render(request, "movies/petitions_index.html", {"template_data": template_data})


@login_required
def petitions_create(request):
    template_data = {"title": "Create Petition"}

    if request.method == "GET":
        return render(request, "movies/petitions_create.html", {"template_data": template_data})

    # POST
    title = request.POST.get("title", "").strip()
    description = request.POST.get("description", "").strip()
    if not title:
        template_data["error"] = "Title is required."
        template_data["form_title"] = title
        template_data["form_description"] = description
        return render(request, "movies/petitions_create.html", {"template_data": template_data})

    Petition.objects.create(
        title=title,
        description=description,
        created_by=request.user,
    )
    messages.success(request, "Petition created.")
    return redirect("movies.petitions_index")


@require_POST
@login_required
def petitions_vote_yes(request, petition_id):
    petition = get_object_or_404(Petition, pk=petition_id)

    # Create vote if not already voted
    _, created = PetitionVote.objects.get_or_create(petition=petition, user=request.user)
    if not created:
        messages.info(request, "You already voted on this petition.")
    else:
        messages.success(request, "Vote recorded. Thanks!")

    return redirect("movies.petitions_index")