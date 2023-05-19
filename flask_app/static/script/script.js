window.addEventListener('DOMContentLoaded', event => {

    const sidebarWrapper = document.getElementById('sidebar-wrapper');
    let scrollToTopVisible = false;
    // Closes the sidebar menu
    const menuToggle = document.body.querySelector('.menu-toggle');
    menuToggle.addEventListener('click', event => {
        event.preventDefault();
        sidebarWrapper.classList.toggle('active');
        _toggleMenuIcon();
        menuToggle.classList.toggle('active');
    })

    // Closes responsive menu when a scroll trigger link is clicked
    var scrollTriggerList = [].slice.call(document.querySelectorAll('#sidebar-wrapper .js-scroll-trigger'));
    scrollTriggerList.map(scrollTrigger => {
        scrollTrigger.addEventListener('click', () => {
            sidebarWrapper.classList.remove('active');
            menuToggle.classList.remove('active');
            _toggleMenuIcon();
        })
    });

    function _toggleMenuIcon() {
        const menuToggleBars = document.body.querySelector('.menu-toggle > .fa-bars');
        const menuToggleTimes = document.body.querySelector('.menu-toggle > .fa-xmark');
        if (menuToggleBars) {
            menuToggleBars.classList.remove('fa-bars');
            menuToggleBars.classList.add('fa-xmark');
        }
        if (menuToggleTimes) {
            menuToggleTimes.classList.remove('fa-xmark');
            menuToggleTimes.classList.add('fa-bars');
        }
    }
})

//show new category input for dashboard
function showCategoryInput() {
    var category = document.querySelector('#category_dashboard')
    if (category.value != 'other' || category.value == 'none') {
        document.querySelector('#create_category').style.display = 'none'
    } else {
        document.querySelector('#create_category').style.display = 'block'
    }
}

//show new category input when creating event/task
const categorySelect = document.querySelector('#select_category')
if (categorySelect != null) {
    categorySelect.addEventListener('change', function () {
        category = document.querySelector('#select_category')
        if (category.value == 'other') {
            document.querySelector('#new_category').innerHTML =
                `<label for="new_category" class="form-label mt-3">Category:</label>
            <div class = "d-flex align-items-center">
                <input type="text" class="form-control" name="category">
                <input type="color" name="color">
            </div>`
        }
    })
}

//show 'reoccurring_freq' for task
function showReoccurringInput() {
    var reoccurring = document.querySelector('#reoccurring_freq')
    reoccurring.style.display = 'block'
}

function hideReoccurringInput() {
    var hide_reoccurring = document.querySelector('#reoccurring_freq')
    hide_reoccurring.style.display = 'none'
}

//trash animation
const trashButtons = document.querySelectorAll('#todo-list a#trash-btn')
console.log(trashButtons)

trashButtons.forEach(button => {
    button.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();
        const li = e.target.closest('li');
        li.classList.add('slide')
        setTimeout(() => li.remove(), 500)
        console.log("target", e.target)
        console.log(e.target.getAttribute("href"))
        fetch(e.target.getAttribute("href"))
        return false;
    })
})


//check animation
const checkButtons = document.querySelectorAll('#todo-list a#check-btn');

checkButtons.forEach(button => {
    button.addEventListener('click', e => {
        const li = e.target.closest('li');
        li.classList.toggle('completed');
    });
});



//date range (for filters)
function getCurrentWeekRange() {
    var curr = new Date;
    var first = curr.getDate() - curr.getDay();
    var last = first + 6;

    var firstday = new Date(curr.setDate(first))
    var lastday = new Date(curr.setDate(last))
    return [firstday, lastday]
}

function getTodayDateRange() {
    var start = new Date();
    start.setUTCHours(0, 0, 0, 0);

    var end = new Date();
    end.setUTCHours(23, 59, 59, 999);
    return [start, end]
}

function getCurrentMonthRange() {
    var date = new Date();
    var firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
    var lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
    return [firstDay, lastDay]
}

//filter
let query = ""
let datePeriod = []
let category = ""
document.getElementById('search').addEventListener('keyup', searchList)
function searchList(event) {
    console.log("searchList")
    query = event.target.value.toLowerCase()
    handleFilteration()
}

const buttons = document.querySelectorAll("#btns-filter button")
for (const btn of buttons) {
    btn.addEventListener("click", handleBtnClick)
}
function handleBtnClick(event) {
    if (event.target.classList.contains("active")) {
        datePeriod = []
        event.target.classList.remove("active")
        handleFilteration()
    } else {
        let filter = event.target.innerText
        if (filter === "This Week") {
            datePeriod = getCurrentWeekRange()
            handleFilteration()
        } else if (filter == "Today") {
            datePeriod = getTodayDateRange()
            handleFilteration()
        } else if (filter === "This Month") {
            datePeriod = getCurrentMonthRange()
            handleFilteration()
        }
        buttons.forEach(btn => btn.classList.remove("active"))
        event.target.classList.add("active")
    }
}

document.getElementById('category_dashboard').addEventListener('change', filterCategory)
function filterCategory(event) {
    category = event.target.value
    if (category === 'none' || category === 'other') {
        event.target.classList.add("active")
        category = ""
    } else {
        event.target.classList.remove("active")
    }
    handleFilteration()
}

function handleFilteration() {
    console.log({ datePeriod, query, category })
    const allLis = document.querySelectorAll('#todo-list > li')
    for (const taskRow of allLis) {
        const taskTitle = taskRow.querySelector("h5 a").innerText.toLowerCase()
        let show = taskTitle.includes(query)
        if (show) {
            if (datePeriod.length > 0) {
                const taskDate = new Date(taskRow.dataset.date);
                const startDate = datePeriod[0]
                const endDate = datePeriod[1]
                if (!(startDate.getTime() <= taskDate.getTime() && endDate.getTime() >= taskDate.getTime())) {
                    show = false
                }
            }
        }

        if (show && category.length > 0) {
            const liCategory = taskRow.dataset.categoryId
            console.log(liCategory, taskRow)
            if (category != liCategory) {
                show = false
            }
        }

        if (show) {
            taskRow.classList.remove("hide")
        } else {
            taskRow.classList.add("hide")
        }
    }
}
