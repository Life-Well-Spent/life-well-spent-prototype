function ResetToHidden(stat, parent_goal_year, parent_goal_year_quarter_month, year, quarter, month, week){
    stat.style.display = "none";
    parent_goal_year.style.display = "none";
    parent_goal_year_quarter_month.style.display = "none";
    year.style.display = "none";
    quarter.style.display = "none";
    month.style.display = "none";
    week.style.display = "none";
}

function EnableField(field){
    field.style.display = "";
}

function UpdateForm(form){
    let time_type_value = form.querySelector("#id_time_type").value;
    let parent_goal_year_value = form.querySelector("#id_parent_goal_year").value;
    
    let parent_goal_year = form.querySelector("#div_id_parent_goal_year");
    let parent_goal_year_quarter_month = form.querySelector("#div_id_parent_goal_year_quarter_month");
    let year = form.querySelector("#div_id_year");
    let quarter = form.querySelector("#div_id_quarter");
    let month = form.querySelector("#div_id_month");
    let week = form.querySelector("#div_id_week");
    let stat = form.querySelector("#div_id_status");

    ResetToHidden(stat,
                  parent_goal_year,
                  parent_goal_year_quarter_month,
                  year,
                  quarter,
                  month,
                  week
    );
    
    switch(time_type_value){
        case "Y":
            EnableField(stat);
            EnableField(year);
            break;
        case "Q":
            if (parent_goal_year_value == ""){
                EnableField(year);
            }

            EnableField(stat);
            EnableField(parent_goal_year);
            EnableField(quarter);
            break;
        case "M":
            if (parent_goal_year_value == ""){
                EnableField(year);
            }

            EnableField(stat);
            EnableField(parent_goal_year);
            EnableField(month);
            break;
        case "W":
            EnableField(stat);
            EnableField(parent_goal_year_quarter_month);
            EnableField(week);
            break;
    }
}

function OnSelectChange(select){
    UpdateForm(select.form);
}

function onLoad(id){
    UpdateForm(document.getElementById(id));
}