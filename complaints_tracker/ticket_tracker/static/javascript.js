$(window).load(function () {
    $(".loader").fadeOut("slow");
});
var table_list = [];
$(function () {
    if (!is_admin) {
        $('#general_filter').css('height', '99%')
    }

    $('#start_date').datepicker({
        dateFormat: "yy-mm-dd"
    });
    $('#end_date').datepicker({
        dateFormat: "yy-mm-dd"
    });
    $('#description_section').find('.detail_section').each(function () {
        update_priority_color(this.id);
        if (this.id == 'resolved_section') {
            table_list.push($('#' + this.id + "_table").dataTable({
                "paging": false,
                "scrollY": "100%",
                "scrollCollapse": true,
                'info': false,
                "dom": '<"hidden_search"f>t'
            }));
            $('#' + this.id + "_table_wrapper").css('height', '85%');
        }
        else {
            table_list.push($('#' + this.id + "_table").dataTable({
                "paging": false,
                "scrollY": "100%",
                "scrollCollapse": true,
                'info': false,
                'filter': false
            }));
            $('#' + this.id + "_table_wrapper").css('height', '74%');
        }
        update_counter(this.id);
    });
    $('.dataTables_scroll').css('height', '100%');
    $(window).bind('resize', function () {
        $(table_list).each(function (i, p) {
            table_list[i].fnAdjustColumnSizing();
        });
    });
    $('#description_section').find('.section_table').find('table').each(function () {
        $('#' + this.id).on('draw.dt', function () {//should be defined earlier to trigger an action when there is a deletion
            $('#description_section').find('.detail_section').each(function () {
                update_counter(this.id);
                $('.dataTables_scrollBody').css('height', '100%');
            });
        });
    });
    $("#popup_complaint_raiser").find("form").on("submit", function (event) {
        if (($('#username_pop').val() && $('#system_id_pop').val() && $('#complaints_pop').val()) == '') {
            event.preventDefault();
            alert('please enter proper values');
        }
        else {
            event.preventDefault();
            $.get($(this).attr('action'), $(this).serialize(), function (data) {
                closeall();
                notification(data);
                var delay = 2000;
                setTimeout(function () {
                    window.location.reload(true);
                }, delay);
            });
        }
    });
    $("#complaints_dialog").button().on("click", function () {
        closeall();
    });
    $('#complaints_dialog').removeClass().addClass('header_right_section').on("mouseover", function () {
        $(this).removeClass().addClass('header_right_section');
    });
    $('#reset').on('click', function () {
        closeall();
    });
    $('.comment_input_region').on('keypress', function () {
        if (event.which == 13) {
            var obj = $(this);
            $(obj).parents('.comment_footer').find('#submit_button').click();
        }
    });
    $('form[name=assigned_to_me_form]').on('click', function () {
        $(this).submit();
    });
    $('form[name=all_issues]').on('click', function () {
        $(this).submit();
    });
    $('form[name=download_csv]').on('click', function () {
        $(this).submit();
    });
    $('#search_in_table').on('keypress click', function () {
        search_in_resolved_table($('#search_in_table').val());
        update_counter('resolved_section');
    });
    $('#mark_resolved_submit').on('click', function () {
        mark_resolve(this);
    });
    $('#mark_resolved_input').blur(function () {
        $('.background_disable').on('click', function () {
            $('#mark_resolved_input').val('');
            $('#resolving_note').fadeOut();
            $('.background_disable').fadeOut();
            ticket_id_for_comments = '';
        });

    });
    remove_double_click($('.resolved_now_column'));
    remove_double_click($('.assigned_to_column'));
    remove_double_click($('.priority_column'));
});
function remove_double_click(obj) {
    var object = obj;
    var chk = $(obj).parents('#resolved_section');
    if ($(chk).length == '0') {
        $(object).dblclick(function () {
            return false;
        });
    }
}
function after_datatabe_initialization() {
    $('.dataTables_scroll').css('height', '100%');
    $(window).bind('resize', function () {
        $(table_list).each(function (i, p) {
            table_list[i].fnAdjustColumnSizing();
        });
    });
}
function notification(string) {
    $('#notification').text(string);
    $('#notification').fadeIn().delay(2000).fadeOut(function () {
        $(this).text('');
    });
}
function closeall() {
    $('#popup_complaint_raiser').fadeToggle();
    $('.background_disable').fadeToggle();
}

function update_counter(section_id) {
    var value = '';
    $(table_list).each(function (i, p) {
        if (table_list[i].attr('id') == section_id + "_table") {
            value = table_list[i].fnSettings().fnRecordsDisplay();
        }
    });
//    var value = $.map($('#' + section_id + ' .highlighted'), function (n, i) {
//        return i;
//    }).length;
    $('#' + section_id).find('.section_label_counter').text(value);
}

function search_in_resolved_table(string) {
    $('#resolved_section_table').DataTable().search(string).draw();

}

function comments_template(d) {
    var comments_template = "" +
        "<div class='inside_comment_body'>" +
        "<span class='date_section'>[" + d['time_of_action'] + "]</span>" +
        "<span class='user_name_section'>[" + d['user_performing_the_act'] + "]</span>" +
        "<span class='comment_section'>" + d['action'] + "</span>" +
        "</div>";
    return comments_template;
}

function comments_template_resolved(d) {
    var comments_template = "" +
        "<div class='inside_comment_body'>" +
        "<span class='date_section'>[" + d['time_of_action'] + "]</span>" +
        "<span class='user_name_section'>[" + d['user_performing_the_act'] + "]</span>" +
        "<span class='comment_section' style='color:cyan'>[Resolved]" + d['action'] + "</span>" +
        "</div>";
    return comments_template;
}


function priority_value(priority) {
    if (priority == "high") {
        return [3, 'red'];
    }
    else if (priority == "medium") {
        return [2, 'blue'];
    }
    else {
        return [1, 'green'];
    }
}

function update_priority_color(section_id) {
    var rows = $('#' + section_id + ' .highlighted');
    for (var i = 0; i < rows.length; i++) {
        var chk = $(rows[i]).find('.priority_selection').val();
        if (chk == '') {
            chk = $(rows[i]).find('.priority_selection').text();
        }
        var priority = priority_value(chk);
        $(rows[i]).find('.priority_selection').css('background-color', priority[1]);

    }
}
function mark_resolve(obj) {
    var data = new Object();
    data.ticket_id = ticket_id_for_comments;
    data.mark_resolved = '1';
    data.comment = $('#mark_resolved_input').val();
    console.log(data);
    if (data.comment != '') {
        $.ajax({
            url: '/ticket_tracker/ajax/update_ticket/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf_token,
                data: JSON.stringify(data)
            },
            success: function (comments) {
                notification('Success fully Marked Resolved');
                var section_id = $(".tickets[ticket_id='" + data.ticket_id + "']").parents('table').attr('id');
                $(".tickets[ticket_id='" + data.ticket_id + "']").find('.complaints_box').parents("tr").fadeOut("slow", function () {
                    var object = this;
                    $(table_list).each(function (i, p) {
                        if (table_list[i].attr('id') == section_id) {
                            var pos = table_list[i].fnGetPosition(object);
                            table_list[i].fnDeleteRow(pos, null, true);//it will automatically redraw the table, and on draw it will trigger the on(draw) function
                        }
                    });
                });
                $('#mark_resolved_input').val('');
                $('#resolving_note').fadeToggle();
                $('.background_disable').fadeToggle();
                ticket_id_for_comments = '';
            },
            error: function (data) {
                alert(data.responseText);
            }
        });
    }
    else {
        notification('please enter valid comment to mark resolved!!');
    }
}
window.priority_update = function (obj) {
    var data = new Object();
    data.priority = $(obj).find('option:selected').val();
    if (data.priority != 'Set Priority') {
        data.ticket_id = $(obj).parents('.tickets').find('.ticket_id').text();
        $.ajax({
            url: '/ticket_tracker/ajax/update_ticket/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf_token,
                data: JSON.stringify(data)
            },
            success: function (comment) {
//                alert(comment.action + ' update priority successfully');
                $(obj).parents('.tickets').next().find('.comment_body').append(comments_template(comment));
                update_priority_color($(obj).parents('.detail_section').attr('id'));
            },
            error: function (data) {
                alert(data.responseText);
            }
        });
    }
}

window.status_update = function (obj) {
    var data = new Object();
    data.status = $(obj).find('option:selected').val();
    data.status_text = $(obj).find('option:selected').text();
    if (data.status != '') {
        data.ticket_id = $(obj).parents('.tickets').find('.ticket_id').text();
        $.ajax({
            url: '/ticket_tracker/ajax/update_ticket/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf_token,
                data: JSON.stringify(data)
            },
            success: function (comment) {
                notification(comment.time_of_action + ' update status successfully');
                $(obj).parents('.tickets').next().find('.comment_body').append(comments_template(comment)); //comments_update
                var section_id = $(obj).parents('table').attr('id');
                $(".tickets[ticket_id='" + data.ticket_id + "']").find('.complaints_box').parents("tr").fadeOut("slow", function () {
                    var object = this;
                    $(table_list).each(function (i, p) {
                        if (table_list[i].attr('id') == section_id) {
                            var pos = table_list[i].fnGetPosition(object);
                            table_list[i].fnDeleteRow(pos, null, true);//it will automatically redraw the table, and on draw it will trigger the on(draw) function
                        }
                    });
                });
            },
            error: function (data) {
                alert(data.responseText);
            }
        });
    }
}

window.engineer_update = function (obj) {
    var div_flag = false;
    var data = new Object();
    data.engineer = $(obj).find('option:selected').val();
    data.engineer_name = $(obj).find('option:selected').text();
    var pattern = /\d+/;
    var pattern2 = /\w+/;
    var update_button = '';
    if (!pattern.test(data.engineer) && !pattern2.test(data.engineer_name)) {
        data.engineer = $(obj).attr('data_engineer_id');
        data.engineer_name = $(obj).attr('data_engineer_name');
        div_flag = true;
        update_button = "" +
            "<button class='mark_assigned'" +
            "data_engineer_id='" + data.engineer + "'" +
            "data_engineer_name='" + data.engineer_name + "'>" + data.engineer_name + "" +
            "</button>";
    }
//    console.log(div_flag);
//    console.log('1', data.engineer, data.engineer_name, pattern.test(data.engineer));
    if (pattern.test(data.engineer) && confirm('Are you sure you want to assign an engineer for this issue?')) {
        data.ticket_id = $(obj).parents('.tickets').find('.ticket_id').text();
        $.ajax({
            url: '/ticket_tracker/ajax/update_ticket/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf_token,
                data: JSON.stringify(data)
            },
            success: function (comment) {
                notification(comment.time_of_action + ' update status successfully');
//                $(obj).parents('.tickets').next().find('.comment_body').append(comments_template(comment));
                if ($(obj).parents('div .detail_section').attr('id') == 'unassigned_section') {
                    var row_displaced = $(".tickets[ticket_id='" + data.ticket_id + "']");
                    var section_id = $(obj).parents('table').attr('id');
                    row_displaced.find('.complaints_box').parents("tr").fadeOut("slow", function () {
                        var object = this;
                        $(table_list).each(function (i, p) {
                            if (table_list[i].attr('id') == section_id) {
                                var pos = table_list[i].fnGetPosition(object);
                                if (div_flag) {
                                    table_list[i].fnUpdate(update_button, pos, 8);
                                }
                                table_list[i].fnUpdate('inprocess', pos, 7);
                                table_list[i].fnDeleteRow(pos, insert_row(object), true);//it will automatically redraw the table, and on draw it will trigger the on(draw) function
                            }
                        });
                    });
//                    row_displaced.insertAfter('#inprocess_section_table tbody tr:first');
                    function insert_row(obj) {
                        $(table_list).each(function (i, p) {
                            if (table_list[i].attr('id') == 'inprocess_section_table') {
                                table_list[i].fnAddData(obj);
                                $(obj).fadeIn();
                                var value = table_list[i].fnSettings().fnRecordsDisplay();//to avoid last column shrink
                                if (value == 1) {
                                    table_list[i].fnAdjustColumnSizing();
                                }
                            }
                        });
                    }

                    row_displaced.find(".status_selection option[value='1']").remove();
                    row_displaced.find('.status_selection').prop('disabled', false);
                    row_displaced.find(".priority_selection option[default]").remove();
                    if (is_user == "TRUE") {
                        $(".tickets[ticket_id='" + data.ticket_id + "']").find('select.engineers_selection').prop('disabled', true);
                    }
                    $('#description_section').find('.detail_section').each(function () {
                        update_counter(this.id);
                        update_priority_color(this.id);
                    });
                }
            },
            error: function (data) {
                alert(data.responseText);
            }
        });
    }
}
var ticket_id_for_comments = '';
window.drop_down_comment = function (obj) {
    $('.background_disable').fadeToggle();
    $('#popup_comments').fadeToggle(300, function () {
        var data = new Object();
        data.ticket_id = $(obj).find('.complaints_box').parents("tr").attr('ticket_id');
        ticket_id_for_comments = $(obj).find('.complaints_box').parents("tr").attr('ticket_id');
        data.comment_popup = '1';
        $.ajax({
            url: '/ticket_tracker/ajax/update_ticket/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf_token,
                data: JSON.stringify(data)
            },
            success: function (comments) {
                $.each(comments, function (index, comment) {
                    $('#ticket_id').text(ticket_id_for_comments);
                    var len = $.map(comment, function (n, i) {
                        return i;
                    }).length;
                    if (len <= 2) {
                        $('.comment_container').find('.issue_subject').append(comment['complaints']);
                    }
                    else if (comment['resolved'] == true) {
                        $('.comment_container').find('.comment_body').append(comments_template_resolved(comment));
                    }
                    else {
                        $('.comment_container').find('.comment_body').append(comments_template(comment));
                    }
                });
                $('.comment_container').find('.comment_body_container').scrollTop(0);
                if (!$('#popup_comments').is(":hidden")) {
                    $('.comment_container').find('input').focus();
                    $('.comment_body_container').animate({ scrollTop: $('.comment_container').find('.comment_body_container').prop('scrollHeight')}, 1000);
                }
            },
            error: function (data) {
                alert(data.responseText);
            }
        });
    });
}

window.close_comment = function (obj) {
    $('.comment_container').find('.issue_subject').text('');
    $('.inside_comment_body').remove();
    $('.comment_container').find('.comment_body_container').scrollTop(0);
    $('#popup_comments').fadeToggle(200);
    $('.background_disable').fadeToggle();
    $('.comment_container').find('input').val('');
    $('#ticket_id').text('');
    ticket_id_for_comments = '';
}

window.post_comment = function (obj) {
    var data = new Object();
    data.comment = $(obj).parents('.comment_footer').find('.comment_input_region').val();
    if (data.comment != '') {
        data.ticket_id = ticket_id_for_comments;
        $.ajax({
            url: '/ticket_tracker/ajax/update_comment/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf_token,
                data: JSON.stringify(data)
            },
            success: function (comment) {
//                alert(comment.time_of_action + ' update status successfully');
                $(obj).parents('.comment_container').find('.comment_body').append(comments_template(comment));
                $(obj).parents('.comment_footer').find('.comment_input_region').val('');
                $(obj).parents('.comment_container').find('.comment_body_container').animate({ scrollTop: $(obj).parents('.comment_container').find('.comment_body_container').prop('scrollHeight')}, 1000);
            },
            error: function (data) {
                alert(data.responseText);
            }
        });
    }
}
window.popup_commit = function (obj) {
    ticket_id_for_comments = $(obj).parents('.tickets').find('.ticket_id').text();
    $('.background_disable').fadeToggle();
    $('#resolving_note').fadeToggle();
    $('#mark_resolved_input').focus();
}

//$(".tickets[ticket_id='1']").appendTo('#resolved_section tbody').find('select.engineers_selection').prop('readonly', true)
//$(".tickets[ticket_id='1']").appendTo('#resolved_section tbody')
//$(".tickets[ticket_id='1']").find('select.engineers_selection').prop('disabled', true)
//$(".tickets[ticket_id='12']").find(".status_selection option[value='1']").remove()
//$.map($('#unassigned_section .highlighted'), function(n, i) { return i; }).length;
//$('.chk').parents('.detail_section').find('.section_label_counter').text('4')
//$('.section_label').width($('detail_section').width())
//$('.section_label').innerWidth()-$('.section_label').width()=ans/2=paddig on 1 side
//b = [a, a = b][0]
//a=[$('#unassigned_section .tickets').first(),$('#unassigned_section .tickets').first().next()]
//b=[$('#inprocess_section .tickets').first(),$('#inprocess_section .tickets').first().next()]
//$.each(a,function(index,value){$(this).insertBefore(b[0]);})
//can call closeall()
//$('.b').scrollTop($('.c').position($('.b').offset()).top)
//            alert('visible');
//            function scrollGo() {
//                var x = $(this).offset().top - 100;
//                $(obj).parents('.section_table').animate({scrollTop: $(obj).parents('.tickets').next('.comments').find('.comment_container').position($(obj).parents('.section_table').offset()).top}, 1000);
//            }
//$(window).bind('resize', function () {
//    p.fnAdjustColumnSizing();
//  } );
