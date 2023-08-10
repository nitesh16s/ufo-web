$(document).ready(function() {
    showSponsers();
    showCountries();
    showActivities();
    showPrograms();
    showLessExplored();
    showWeekendAdventure();
})


function showSponsers() {
    $.ajax({
        url: '/sponsers',
        success: function(data) {
            $('#sponsers').html('')
            data.forEach(element => {
                $('#sponsers').append('<div class="col-md-3"><a href="' + element.url + '"><img style="width:150px; height: auto;" src="/media/' + element.image + '" alt=""></a></div>')
            })
        }
    })
}

function showMore(id) {
    $('#' + id).toggleClass('hide')
    $('#drop_' + id + '_plus').toggleClass('hide')
    $('#drop_' + id + '_minus').toggleClass('hide')
}

// nav functions start
function showCountries() {
    $.ajax({
        url: '/show-countries',
        success: function(data) {
            $('#countries').html('')
            $('#countriesM').html('')
            data.forEach(country => {
                // nav web
                $('#countries').append('<li><a class="dropdown-item" href="/' + country.slug + '/' + '" onmouseover="showPackages(' + country.id + ')">' + country.country + '</a><ul class="submenu dropdown-menu"><li id="country_packages' + country.id + '"><a>Fetching country packages</a></li></ul></li>');
                // nav mobile
                $('#countriesM').append('<ul><li><a onclick="showPackages(' + country.id + ')">' + country.country + '</a><ul><li id="country_packagesM' + country.id + '"></li></ul></li></ul>')
            })
        }
    })
}


function showPackages(country_id) {
    $.ajax({
        url: '/show-country-packages/' + country_id + '',
        success: function(data) {
            if (data.length > 0) {
                $('#country_packages' + country_id).html('')
                $('#country_packagesM' + country_id).html('')
                data.forEach(package => {
                    // nav web
                    $('#country_packages' + country_id).append('<a href=/' + package.country__slug + '/' + package.region__slug + '/' + package.slug + '>' + package.name + '</a></li>');
                    // nav mobile
                    $('#country_packagesM' + country_id).append('<li><a href=/' + package.country__slug + '/' + package.region__slug + '/' + package.slug + '>' + package.name + '</a></li>')
                });
            } else {
                // nav web
                $('#country_packages' + country_id).html('<a>No Package Available</a>');
                // nav mobile
                $('#country_packagesM' + country_id).html('<li><a>No Package Available</a></li>')
            }
        }
    })
}


function showActivities() {
    $.ajax({
        url: '/show-activities',
        success: function(data) {
            $('#activities').html('')
            $('#activitiesM').html('')
            $('#activitiesF').html('')
            data.forEach(element => {
                // nav web
                $('#activities').append('<a class="dropdown-item" href="/activity/' + element.fields.slug + '">' + element.fields.activity + '</a>');
                // nav mobile
                $('#activitiesM').append('<li><a class="dropdown-item" href="/activity/' + element.fields.slug + '">' + element.fields.activity + '</a></li>')
                    // footer
                $('#activitiesF').append('<li><a class="dropdown-item" href="/activity/' + element.fields.slug + '">' + element.fields.activity + '</a></li>')
            })
        }
    })
}


function showPrograms() {
    $.ajax({
        url: '/show-training-programs',
        success: function(data) {
            $('#training_programs').html('');
            $('#training_programsM').html('');
            $('#training_programsF').html('');
            if (data.length > 0) {
                data.forEach(program => {
                    // nav web
                    $('#training_programs').append('<a class="dropdown-item" href=/training-programs/' + program.slug + '>' + program.name + '</a>');
                    // nav mobile
                    $('#training_programsM').append('<li><a class="dropdown-item" href=/training-programs/' + program.slug + '>' + program.name + '</a></li>');
                    // footer
                    $('#training_programsF').append('<li><a class="dropdown-item" href=/training-programs/' + program.slug + '>' + program.name + '</a></li>');
                })
            } else {
                // nav web
                $('#training_programs').append('<a>No Training Programs.</a>');
                // nav mobile
                $('#training_programsM').append('<li><a>No Training Programs.</a></li>');
            }
        }
    })
}

function showLessExplored() {
    $.ajax({
        url: '/show-less-explored',
        success: function(data) {
            $('#less_explored').html('')
            $('#less_exploredM').html('')
            $('#less_exploredF').html('')
            if (data.length > 0) {
                data.forEach(package => {
                    // nav web
                    $('#less_explored').append('<a class="dropdown-item" href=/' + package.country__slug + '/' + package.region__slug + '/' + package.slug + '>' + package.name + '</a>');
                    // nav mobile
                    $('#less_exploredM').append('<li><a class="dropdown-item" href=/' + package.country__slug + '/' + package.region__slug + '/' + package.slug + '>' + package.name + '</a></li>');
                    // footer
                    $('#less_exploredF').append('<li><a class="dropdown-item" href=/' + package.country__slug + '/' + package.region__slug + '/' + package.slug + '>' + package.name + '</a></li>');
                })
            } else {
                // nav web
                $('#less_explored').html('<a>No Package.</a>');
                // nav mobile
                $('#less_exploredM').html('<li><a>No Package.</a></li>');
            }
        }
    })
}


function showWeekendAdventure() {
    $.ajax({
        url: '/show-weekend-adventures',
        success: function(data) {
            $('#weekend_adventures').html('')
            $('#weekend_adventuresM').html('')
            $('#weekend_adventuresF').html('')
            if (data.length > 0) {
                data.forEach(package => {
                    // nav web
                    $('#weekend_adventures').append('<a class="dropdown-item" href=/weekend-adventure/' + package.slug + '>' + package.name + '</a>');
                    // nav mobile
                    $('#weekend_adventuresM').append('<li><a class="dropdown-item" href=/' + package.country__slug + '/' + package.region__slug + '/' + package.slug + '>' + package.name + '</a></li>');
                    // footer
                    $('#weekend_adventuresF').append('<li><a class="dropdown-item" href=/' + package.country__slug + '/' + package.region__slug + '/' + package.slug + '>' + package.name + '</a></li>');
                })
            } else {
                // nav web
                $('#weekend_adventures').html('<a>No Weekend Adventure.</a>');
                // nav mobile
                $('#weekend_adventures').html('<li><a>No Weekend Adventure.</a></li>');
            }
        }
    })
}
// nav functions end


// index search start
function showTrips() {
    var entry = document.getElementById('perfectTrips').value;
    if (entry.length > 0) {
        $('#perfectTripsResults').removeClass('hide')
        $.ajax({
            url: '/perfect-trips/' + entry,
            success: function(data) {
                $('#perfectTripsResults').html('')
                data.forEach(package => {
                    $('#perfectTripsResults').append('<a href=/' + package.country__slug + '/' + package.region__slug + '/' + package.slug + '>' + package.name + '</a><br><hr>')
                })
            }
        })
    } else {
        $('#perfectTripsResults').addClass('hide')
    }
}
// index search end


function saveBlog(id) {
    $.ajax({
        url: '/blog/' + id + '/save',
        success: function(data) {
            if (data.msg == 'Unsaved') {
                $('#saveBlog').html('<i class="fa fa-bookmark-o"></i> Save')
            } else {
                $('#saveBlog').html('<i class="fa fa-bookmark"></i> Unsave')
            }
        }
    })
}


function likeBlog(id) {
    $.ajax({
        url: '/blog/' + id + '/like',
        success: function(data) {
            if (data.msg == 'Disliked') {
                $('#likeBlog').html('<i class="fa fa-heart-o"></i> ' + data.total_likes)
            } else {
                $('#likeBlog').html('<i class="fa fa-heart"></i> ' + data.total_likes)
            }
        }
    })
}


function follow(id) {
    $.ajax({
        url: '/accounts/friendships/' + id + '/follow',
        success: function(data) {
            if (data.msg == 'Unfollowed') {
                $('#follow').html('Follow')
            } else {
                $('#follow').html('Unfollow')
            }
        }
    })
}


function showReplies(id) {
    $('#' + id + 'replyDiv').toggleClass('hide')
    $.ajax({
        url: '/blog/comment/' + id + '/replies',
        success: function(data) {
            if (data['replies'] === 0) {
                $('#' + id + 'replyDiv').html('No replies yet')
            } else {
                $('#' + id + 'replyDiv').html('<div class="author-image"><img style="height: 70px; width: 70px; border-radius: 50%;"  src="/media/' + data['profile_picture'] + '" alt=""></div><div class="comment-text"><div class="author-info"><h4><a href="#">' + data['username'] + '</a></h4><span class="reply"><a onclick="showReplies(' + id + ')"><i class="fa fa-reply"></i>Hide Replies</a></span><span class="comment-time">' + data['createdAt'] + '</span></div><p id="reply">' + data['content'] + '</p></div>')
            }
        },
    })
}


function availableSeats(pid, sid) {
    $('#availableSeats' + sid).html('Fetching available seats...')
    $.ajax({
        url: '/packages/' + pid + '/' + sid + '/' + 'available-seats',
        success: function(data) {
            $('#availableSeats' + sid).html('<a><small><b>' + data['available'] + '</b></small></a><hr>')
            if (data['available'] > 0) {
                $('#book-seat' + sid).toggleClass('hide')
            } else {
                $('#no-seats' + sid).html('<a>No Seats</a><hr>')
            }
        }
    })
}


function addComment(id) {
    var data = new FormData();
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val()
    $.ajax({
        url: '/blog/' + id + '/new/comment',
        data: data,
        csrfmiddlewaretoken: csrfToken,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data) {
            alert(data);
        }
    });
}

function showComments(blog_id) {
    $('#user_comments').html('Fetching Comments...')
    $.ajax({
        url: '/blog/' + blog_id + '/comments',
        success: function(data) {
            $('#user_comments').html('')
            data.forEach(comment => {
                $('#user_comments').append('<div class="single-comment"><div class="author-image"><img style="height: 70px; width: 70px; border-radius: 50%;" src="" alt=""></div><div class="comment-text"><div class="author-info"><h4><a href="#">' + comment.fields.author + '</a></h4><span class="reply"><a onclick="showReplies(' + comment.pk + ')"><i class="fa fa-reply"></i>Show Replies</a></span><span class="comment-time">' + comment.fields.createdAt + '</span></div>' + comment.fields.content + '</div></div><div id="' + comment.pk + 'replyDiv" class="single-comment comment-reply hide">Fetching Replies...</div>')
            });
        }
    })
}


function updateProfile() {
    alert('aaaaaa')
}


function showAnswers(id) {
    $.ajax({
        url: '/accounts/query/' + id + '/answers',
        success: function(data) {
            $('#answers').html('');
            data.forEach(answer => {
                $('#answers').prepend(answer.fields.answer + '<hr>')
            })
        }
    })
}