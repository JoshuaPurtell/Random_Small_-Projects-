using JuMP
using GLPK
using MathOptInterface
const MOI = MathOptInterface



function optimal_stakes(p_U_S,p_U_F,generosity=0,gen_weight=0) #probability with which shaurya thinks UP will win, ditto with friend
    #1 represents shaurya being generous, -1 represents friend being generous, 0 represents neither
    #gen_weight = 1 perfectly generous, gen_weight = 0 not at all generous
    lambda = (p_U_S+p_U_F)/2

    betting_model = Model(optimizer_with_attributes(GLPK.Optimizer, "tm_lim" => 60000, "msg_lev" => GLPK.OFF))

    @variable(betting_model, payoff_shaurya_UP)
    @variable(betting_model, payoff_shaurya_nUP)

    @constraint(betting_model, risk_constraint1, -1 >= payoff_shaurya_UP >= -50)
    @constraint(betting_model, risk_constraint2, 50 >= payoff_shaurya_nUP >= 1)
    @constraint(betting_model, fairness_constraint, lambda*payoff_shaurya_UP +(1-lambda)*payoff_shaurya_nUP == 0)

    @objective(betting_model, Max, payoff_shaurya_nUP)

    status = optimize!(betting_model)
    print(termination_status(betting_model))
    println("fair bet:", value(payoff_shaurya_UP), " ",value(payoff_shaurya_nUP))
    println("Shaurya expects to break even:", -50, " ",50)
    println("Friend expects to break even:", -21.42, " ",50)
    if (generosity == 1)
        final_payoff_shaurya_UP = (1-gen_weight)*value(payoff_shaurya_UP) + gen_weight*-50
        final_payoff_shaurya_nUP = (1-gen_weight)*value(payoff_shaurya_nUP) + gen_weight*50
    end
    if (generosity == -1)
        final_payoff_shaurya_UP = (1-gen_weight)*value(payoff_shaurya_UP) + gen_weight*-21.42
        final_payoff_shaurya_nUP = (1-gen_weight)*value(payoff_shaurya_nUP) + gen_weight*50
    end
    if (generosity == 0)
        final_payoff_shaurya_UP = value(payoff_shaurya_UP)
        final_payoff_shaurya_nUP = value(payoff_shaurya_nUP)
    end
    println("Your bet:", final_payoff_shaurya_UP, " ",final_payoff_shaurya_nUP)
end

optimal_stakes(.5,.7)
optimal_stakes(.5,.7,1,.8)
#(-50,50) is breakeven under shaurya's expectation
#(-21.42,50) is breakeven under friends's expectation
# if one side is feeling generous, take an \theta*(breakeven_generous) + (1-\theta)*(optimal) for appropriate \theta \in (0,1)
