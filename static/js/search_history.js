var date1, date2 = ''

  
let list = document.getElementById("myList");
let url = "http://127.0.0.1:8000/filter-resuls/?q=hello"
  

var values=''
// get selected item form user  
$(document).ready(function(){
    $('input[name="user"]').on('change', function() {
        $('input[name="user"]').not(this).prop('checked', false);
        
        if($('input[name="user"]:checked').val()===undefined){ 
            const updateUrl = url.replace(values, "");
            url=updateUrl
            fetched_filterd_data(updateUrl)
        }else{ 
            const value = $('input[name="user"]:checked').val()
            if (values){

                url= url.replace(values, "");
            } 
            values = '&user='+value
            url =  url+values
            fetched_filterd_data(url)
        }

    });
});


// get selected item form keyward 
var keys=''
$(document).ready(function(){
    $('input[name="keyword"]').on('change', function() {
        $('input[name="keyword"]').not(this).prop('checked', false);
        console.log($('input[name="keyword"]:checked').val())
        if($('input[name="keyword"]:checked').val()===undefined){
            url=url.replace(keys, "");
            fetched_filterd_data(url)
        }else{
            const value = $('input[name="keyword"]:checked').val()
            if (keys){
                url= url.replace(keys, "");
            } 
            keys = '&keyword='+value
            url = url+keys
            fetched_filterd_data(url)
        }
    });
});


// get selected item form data 
var datas=''
$(document).ready(function(){
    $('input[name="data"]').on('change', function() {
        $('input[name="data"]').not(this).prop('checked', false);
        console.log($('input[name="data"]:checked').val())
        if($('input[name="data"]:checked').val()===undefined){ 
            const updateUrl = url.replace(datas, "");
            url=url.replace(datas, "");
            fetched_filterd_data(url)
        }else{

            if (date1 && date2){
                url= url.replace(date1, "");
                url= url.replace(date2, "");
            }

            const value = $('input[name="data"]:checked').val()
            if (datas){
                url= url.replace(datas, "");
            } 
            datas = '&data='+value
            url = url+datas
            fetched_filterd_data(url)
        }
    });
});





// get selected date

// start Date
const startDate = document.querySelector('#start');

startDate.addEventListener('change', (event) => {
    
    $('input[name="data"]').not(this).prop('checked', false);
    const updateUrl = url.replace(datas, "");
    url=updateUrl

    var dateControl1 = document.querySelector('#start');

    var dateControl2     = document.querySelector('#end');
    console.log(dateControl2.value);
    if (!dateControl2.value){
        document.getElementById("alart").innerText="Please select the end Date"
    }else{
        document.getElementById("alart").innerText=""
        
        if (date1 && date2){
            url= url.replace(date1, "");
            url= url.replace(date2, "");
        }
        
        date1='&startDate='+dateControl1.value
        date2='&endDate='+dateControl2.value
        url = url+date1+date2
        fetched_filterd_data(url)

    }
  });


// end Date
const endDate = document.querySelector('#end');
endDate.addEventListener('change', (event) => {
    $('input[name="data"]').not(this).prop('checked', false);
    const updateUrl = url.replace(datas, "");
    url=updateUrl

      var dateControl1 = document.querySelector('#start');
      console.log(dateControl1.value);
      

      var dateControl2 = document.querySelector('#end');
      console.log(dateControl2.value);

    if (!dateControl1.value){
        document.getElementById("alart").innerText="Please select the Start Date"
    }else{
        document.getElementById("alart").innerText=""
        console.log('hello');
        console.log(date2, 'date 2 is here');
        if (date1 && date2){
            url= url.replace(date1, "");
            url= url.replace(date2, "");
        }
        date1='&startDate='+dateControl1.value
        date2='&endDate='+dateControl2.value

        url = url+date1+date2
        fetched_filterd_data(url)
    }


});


    fetch("http://127.0.0.1:8000/filter-resuls/?q=hello", {
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
        },
    })
    .then(response => {
        return response.json() //Convert response to JSON
    })
    .then(data => {
        // console.log(data['filterd_items']);
        $('#myList').empty();
        data['filterd_items'].forEach(data=>{
            let li = document.createElement("li");
            li.innerHTML = " <p id='search_history'>"
            +"<span id='link' class='site-link' style='font-size:12px'>"+ data.site_link+"</span><br/>"
            +"<strong><a id='title' href='"+data.site_link+"' target='_blank' class='button is-info'>"+ data.site_title+"</a></strong><br/>"
            +"<span id='dec'>"+ data.site_description+"</span>"
          +"</p>" 
            
              list.appendChild(li);
        })
        
        //Perform actions with the response data from the view
    })


    const fetched_filterd_data = (url) =>{
        console.log(url);
        fetch(url, {
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
        },
    })
    .then(response => {
        return response.json() //Convert response to JSON
    })
    .then(data => {
        // console.log(data['filterd_items']);
        console.log( data['empty']);
        if (data['empty']==='No result found for this query'){
            $('#myList').empty();
            let li = document.createElement("li");
            li.innerHTML ="<p id='search_history' style='color:green'><h3>"+data['empty']+"</h3></p>"
            list.appendChild(li);
        }else{      
        $('#myList').empty();
        data['filterd_items'].forEach(data=>{
            let li = document.createElement("li");
            li.innerHTML = " <p id='search_history'>"
            +"<span id='link' class='site-link' style='font-size:12px'>"+ data.site_link+"</span><br/>"
            +"<strong><a id='title' href='"+data.site_link+"' target='_blank' class='button is-info'>"+ data.site_title+"</a></strong><br/>"
            +"<span id='dec'>"+ data.site_description+"</span>"
          +"</p>" 
            
              list.appendChild(li);
        })}
        
        //Perform actions with the response data from the view
    })
    }