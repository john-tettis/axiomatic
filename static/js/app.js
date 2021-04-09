
$('.fa-heart').on('click', function(e){
    let temp = $(e.target).parent().parent().parent().parent().parent()
    let content = temp.find('p').text()
    let author = temp.find('.author').text()
    likeQuote(content,author)
    updateHeart($(e.target))
    
})

$('.fa-share').on('click', function(e){
    let temp = $(e.target).parent().parent().parent().parent().parent()
    let content = temp.find('p').text()
    let author = temp.find('.author').text()
    shareQuote(content,author)
    window.location.replace("/reposted");

})


$('.fa-minus-circle').on('click', function(e){
    let temp = $(e.target).parent().parent().parent().parent().parent()
    let content = temp.find('p').text()
    let author = temp.find('.author').text()
    console.log(author,content)
    unshareQuote(content,author)
    temp.parent().remove()
})




function likeQuote(content, author){
    axios.post('/quotes/like',{
        content:content,
        author:author
    }).then(function(response){
        console.log(response)
    })
}
function shareQuote(content, author){
    axios.post('/quotes/share',{
        content:content,
        author:author
    }).then(function(response){
        console.log(response)
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