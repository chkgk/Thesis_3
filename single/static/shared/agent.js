$('.otree-btn-next').hide();
var touched =  {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
};

function check_all_sliders_touched(num_sliders) {
    sum = 0;
    for (e in touched) {
        sum += touched[e];
    }
    return (sum == num_sliders);
}

$("#id_decision_for_p1").slider();
// $("#id_invest_client_2").slider();
// $("#id_invest_client_3").slider();
// $("#id_invest_client_4").slider();


function calc_client_payoffs(risky) {
    var safe = 10 - risky;

    var good_state = safe + risky*3.5;
    var bad_state = safe;

    return {'win': good_state, 'lose': bad_state};
}

function calc_advisor_payoffs(risky) {
    var fixed_pay = {{ Constants.fixed_payment|json }};
    var compensation = {{ player.compensation|json }};
    var share_result = {{ Constants.share_result|json }};
    var share_profit = {{ Constants.share_profit|json }};
    var client_payoffs = calc_client_payoffs(risky);

    if (compensation == 'fixed') {
        return {'win': 5, 'lose': 5, 'ev': 5};
    } else if (compensation == 'variable_result') {
        return {
            'win': fixed_pay + client_payoffs['win']*share_result/100, 
            'lose': fixed_pay + client_payoffs['lose']*share_result/100, 
        };
    } else { // variable_profit
        return {
            'win': fixed_pay + risky*2.5*share_profit/100,
            'lose': fixed_pay,
        };
    }
}

$('#id_decision_for_p1').on('change', function (event) {
    change_table(event);
});

$('.slider-handle').hide();
$('.slider').on('mousedown', function (event) {
    $(this).find('.slider-handle:not(.hide)').show();
});

// $('#id_invest_client_2').on('change', function (event) {
//     change_table(event);
// });

// $('#id_invest_client_3').on('change', function (event) {
//     change_table(event);
// });

// $('#id_invest_client_4').on('change', function (event) {
//     change_table(event);
// });

function change_table(event) {
    var client_payoffs = calc_client_payoffs(event.target.value);
    var advisor_payoffs = calc_advisor_payoffs(event.target.value);

    var id = event.target.id.slice(-1);
    //console.log(id);

    touched[id] = 1;

    $('#safe_'+id).html((10 - event.target.value).toFixed(2)+'€');
    $('#risky_'+id).html(parseFloat(event.target.value).toFixed(2)+'€');

    $('#lose_'+id).html(client_payoffs['lose'].toFixed(2)+'€');
    $('#win_'+id).html(client_payoffs['win'].toFixed(2)+'€');

    $('#pay_lose_'+id).html(advisor_payoffs['lose'].toFixed(2)+'€');
    $('#pay_win_'+id).html(advisor_payoffs['win'].toFixed(2)+'€');
    //$('#pay_ev_'+id).html(advisor_payoffs['ev'].toFixed(2));

    // var ev = calc_sums();
    // $('#ev').html(ev.toFixed(2));

    if (check_all_sliders_touched(1)) {
        $('.otree-btn-next').show();
    }
}

function calc_sums() {
    var ev_sum = 0;

    for (var id = 1; id < 5; id++) {
        loss = parseFloat($('#pay_lose_'+id).html());
        win = parseFloat($('#pay_win_'+id).html());
        ev_sum += (loss * 2/3) + (win * 1/3);
    }

    return ev_sum;
}