
$('.fa-heart').on('click', function(e){
    let temp = $(e.target).parent().parent().parent().parent().parent()
    let content = temp.find('.quote-content').first().text()
    let author = temp.find('.author').text()
    likeQuote(content, author, $(e.target))
})
// $(document).ready(function() {
//     $("#mymodal").modal();
//   });

$('.fa-share').on('click', function(e){
    let temp = $(e.target).parent().parent().parent().parent().parent()
    let content = temp.find('.quote-content').first().text()
    let author = temp.find('.author').text()
    console.log(content)
    shareQuote(content,author,$(e.target))
})

$('.comment').on('click', function(e){
    e.preventDefault()
    let $input = $(e.target).parent().find('input')
    let content = $input.val()
    let author = $input.data('quote')
    $input.val('')
    let qc = $(e.target).parent().parent().parent().parent().parent().find('.quote-content').text()
    console.log(content, author, qc)
    addComment(content,author, qc)

})

$('.fa-minus-circle').on('click', function(e){
    let temp = $(e.target).parent().parent().parent().parent().parent()
    let content = temp.find('.quote-content').first().text()
    let author = temp.find('.author').text()
    console.log(author,content)
    unshareQuote(content,author)
    updateRepost($(e.target))
})




async function likeQuote(content, author,target){
    return await axios.post('/quotes/like',{
        content:content,
        author:author
    }).then(function(response){
        if(response.data['message'] === 'Not logged in'){
            alert('You must log in to like a quote')
        }
        else{
            updateHeart(target)
        }
    })
}
function shareQuote(content, author,target){
    return axios.post('/quotes/share',{
        content:content,
        author:author
    }).then(function(response){
        console.log(response)
        if(response.data['message'] === 'Not logged in'){
            console.log(response)
            alert('You must log in to share a quote')
        }
        else{
            updateRepost(target)
        }
        
    })
}
function unshareQuote(content, author){
    axios.delete('/quotes/share',{
        data:{
            content:content,
            author:author
        }
    }).then(function(response){
        console.log(response)
    })
}

function updateHeart(target){
    console.log(target.hasClass('far'))
    if(target.hasClass('far')){
        target.removeClass('far')
        target.addClass('fas')
    }
    else if(target.hasClass('fas')){
        target.removeClass('fas')
        target.addClass('far')
    }
}

function addComment(content,author,qc){
    axios.post('/comments/add',{
        content:content,
        author:author,
        quote_content:qc.trim()
    }).then(function(response){
        console.log(response)
    })

}

function updateRepost(target){
    console.log(target.hasClass(''))
    if(target.hasClass('fa-minus-circle')){
        target.removeClass('fa-minus-circle')
        target.addClass('fa-share')
    }
    else if(target.hasClass('fa-share')){
        target.removeClass('fa-share')
        target.addClass('fa-minus-circle')
    }
}