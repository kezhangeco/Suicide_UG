libname ug 'e:\';

proc import datafile="e:\ug_gee_covars N129 mark 5.dta" out=ug.ug_geeOrig dbms=dta replace;
run;

*proc import datafile="e:\ug_gee_covars N129 mark 2.sav" out=ug.ug_geeOrig dbms=sav replace;
*run;


proc contents data=ug.ug_geeOrig;
run;

PROC FORMAT;
  VALUE  grp 1="Control"
             2="NS Depressed"
			 4="Ideator"
			 6="Low Leth"
			 7="High Leth";
	VALUE stake 0="low (<=10)"
				1="high (>10)";
	VALUE fairness 1="v unf"
		2 = "m unf"
		3 = "fair";
RUN;

*ensure that we have groups sorted ascending;
proc sort data = ug.ug_geeOrig;
by Group12467 ID trial;
run;

/*proc print data=ug.ug_geeOrig (obs=20);
	var Group12467 ID stake trial accept;
run;

proc means data = ug.ug_geeOrig;
	var IIP15INTAMBV BIS_nonplan ageatconsent;
run;*/

data ug.ug_geeOrig;
	set ug.ug_geeOrig;
	iipAmbiv_c = IIP15INTAMBV - 5.1296296;
	BIS_nonplan_c = BIS_nonplan - 17.1083333;
	ageatconsent_c = ageatconsent - 64.8837209;
	trial = trial - 1; *shift trial to 0-23 so that intercept represents effect at trial 1;
	trialSq = trial**2;
	log_income=log(SES_income_percap); *log transform normalizes this;
run;

/*proc freq data = ug.ug_geeOrig;
	table trial trialSq;
run;*/

*GEE APPROACH;
ods html close;
ods html;
*ar1;
proc genmod data=ug.ug_geeOrig descending order=formatted;
	class ID trial fairness Group12467 stake;
    model  accept = fairness | stake | Group12467 / dist=bin type3;
    repeated subject=ID / type=ar within=trial corrw; *covb;
run;

*unstructured -- blows up;
proc genmod data=ug.ug_geeOrig descending order=formatted;
	class ID trial fairness Group12467 stake;
    model  accept = fairness | stake | Group12467 / dist=bin type3;
    repeated subject=ID / type=un within=trial corrw; *covb;
run;

*compound symmetry / exchangeable;
ods pdf file='e:\ug_geeCS_withContrasts_11Dec2012.pdf';
proc genmod data=ug.ug_geeOrig descending order=formatted;
	class ID trial fairness Group12467 stake;
    model  accept = fairness | stake | Group12467 / dist=bin type3;
    repeated subject=ID / type=exch within=trial corrw; *covb;
	estimate 'LS hi-lo stk: ctl vs. high leth' Group12467*stake
		-1 1
		0 0
		0 0
		0 0
		1 -1; * /cov corr e elsm;
	estimate 'LS hi-lo stk in high leth' Group12467*stake
		0 0
		0 0
		0 0
		0 0
		1 -1; * /cov corr e elsm;
	lsmeans stake*Group12467 /diff pdiff adjust=tukey plots=meanplot;
	slice stake*Group12467 /sliceBy=Group12467 diff adjust=tukey plots=meanplot(sliceby=Group12467 join);
	format Group12467 grp. stake stake.;
run;
ods pdf close;


*5-dep;
proc genmod data=ug.ug_geeOrig descending order=formatted;
	class ID trial fairness Group12467 stake;
    model  accept = fairness | stake | Group12467 / dist=bin type3;
    repeated subject=ID / type=mdep(5) within=trial corrw; *covb;
run;

*independent;
proc genmod data=ug.ug_geeOrig descending order=formatted;
	class ID trial fairness Group12467 stake;
    model  accept = fairness | stake | Group12467 / dist=bin type3;
    repeated subject=ID / type=indep within=trial corrw; *covb;
run;


*basic GLMM with group, fairness, and stakep;
*VC structure;
*just allow for random intercept;
*ods html close;
*ods html;
ods pdf file='e:\ug_glmms_basic.pdf';
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=formatted method=quad(qpoints=8); *need order internal to avoid being sorted alphabetically;
		title 'group x fairness x stake GLMM: intercept only';
		class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 /solution dist=binary link=logit; * ddfm=kr;
        random intercept /sub=ID type=VC G;
		nloptions technique=newrap;
		format Group12467 grp. stake stake. fairness fairness.;
run;

*uncorrelated intercept and trial effects;
*THIS IS THE BEST MODEL IN TERMS OF AIC/BIC FIT;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=formatted method=quad(qpoints=8); *laplace;  *need order internal to avoid being sorted alphabetically;
		title 'group x fairness x stake GLMM: uncor intercept + trial RE';
		class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 /solution dist=binary link=logit ddfm=betwithin;
        random intercept trial /sub=ID type=VC G; *cs says to allow intercept and trial to covary;
		nloptions technique=newrap maxiter=200;
		format Group12467 grp. stake stake. fairness fairness.;
run;

*uncorrelated intercept and trial effects, add fixef trial;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=formatted method=quad(qpoints=8); *laplace;  *need order internal to avoid being sorted alphabetically;
		title 'group x fairness x stake GLMM: uncor intercept + trial RE, fixef trial';
		class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 trial /solution dist=binary link=logit; * ddfm=kr;
        random intercept trial /sub=ID type=VC G; *cs says to allow intercept and trial to covary;
		nloptions technique=newrap maxiter=200;
		format Group12467 grp. stake stake. fairness fairness.;
run;


ods html close;
ods html;
/*
This is as close as I can get to GLMER

i.e.,
1) using correlated intercept + trial random effects (type UN allows correlation)
2) using AGQ with 8 points
3) estimates are generally quite similar, both fixed and random

N.B.: leave trial out of class statement to avoid unique estimate for each trial (as opposed to a distribution around trial effect)
*/

proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=formatted method=quad(qpoints=8); *laplace;  *need order internal to avoid being sorted alphabetically;
		title 'group x fairness x stake GLMM: corr intercept + trial RE';
		class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 /solution dist=binary link=logit; * ddfm=kr;
        random intercept trial /sub=ID type=UN G; *un says to allow intercept and trial to covary;
		nloptions technique=newrap maxiter=200;
		format Group12467 grp. stake stake. fairness fairness.;
run;


proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=formatted method=quad(qpoints=8); *laplace;  *need order internal to avoid being sorted alphabetically;
		title 'group x fairness x stake GLMM: corr intercept + trial RE, fixef trial';
		class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 trial /solution dist=binary link=logit; * ddfm=kr;
        random intercept trial /sub=ID type=UN G; *un allows for intercept and trial effects to be correlated;
		nloptions technique=newrap maxiter=200;
		format Group12467 grp. stake stake. fairness fairness.;
run;

*include linear and quadratic terms for trial, as well as corresponding REs.;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=formatted method=quad(qpoints=8); *laplace;  *need order internal to avoid being sorted alphabetically;
        title 'group x fairness x stake GLMM: corr intercept + trial + trial^2 RE, fixef trial + trial^2';
		class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 trial trialSq /solution dist=binary link=logit; * ddfm=kr;
        random intercept trial trialSq /sub=ID type=VC G; *VC forces intercept, trial, and trialSq REs to be uncorrelated;
		nloptions technique=newrap maxiter=200;
		format Group12467 grp. stake stake. fairness fairness.;
run;

*include linear and quadratic terms for trial, as well as corresponding REs.;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=formatted method=quad(qpoints=8); *laplace;  *need order internal to avoid being sorted alphabetically;
        title 'group x fairness x stake GLMM: corr intercept + trial + trial^2 RE, no trial fixefs';
		class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 /solution dist=binary link=logit; * ddfm=kr;
        random intercept trial trialSq /sub=ID type=VC G; *cs says to allow intercept and trial to covary;
		nloptions technique=newrap maxiter=200;
		format Group12467 grp. stake stake. fairness fairness.;
run;

ods pdf close;

*moving forward (as we conduct contrasts and add covariates), use a intercept + trial RE model with no FE trial, no correlation among intercept and trial effects;


*add age at consent;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=formatted method=quad(qpoints=8); *laplace;  *need order internal to avoid being sorted alphabetically;
		title 'group x fairness x stake GLMM: uncor intercept + trial RE';
		class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 fairness|ageatconsent /solution dist=binary link=logit ddfm=betwithin;
        random intercept trial /sub=ID type=VC G; *vc does not allow intercept and trial REs to covary;
		nloptions technique=newrap maxiter=200;
		format Group12467 grp. stake stake. fairness fairness.;
run;

*add sex;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=formatted method=quad(qpoints=8); *laplace;  *need order internal to avoid being sorted alphabetically;
		title 'group x fairness x stake GLMM: uncor intercept + trial RE';
		class fairness Group12467 stake gender; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 fairness|ageatconsent fairness|stake|gender /solution dist=binary link=logit ddfm=betwithin;
        random intercept trial /sub=ID type=VC G; *vc does not allow intercept and trial REs to covary;
		nloptions technique=newrap maxiter=200;
		format Group12467 grp. stake stake. fairness fairness.;
run;


*now add SES/income;
*N.B. 19 people are missing this information! This yields a different sample here...;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=formatted method=quad(qpoints=8); *laplace;  *need order internal to avoid being sorted alphabetically;
		title 'group x fairness x stake GLMM: uncor intercept + trial RE';
		class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 fairness|ageatconsent fairness|stake|log_income /solution dist=binary link=logit ddfm=betwithin;
        random intercept trial /sub=ID type=VC G; *vc does not allow intercept and trial REs to covary;
		nloptions technique=newrap maxiter=200;
		format Group12467 grp. stake stake. fairness fairness.;
run;

*income is horribly skewed, with one person way above the rest;
data onetrial;
	set ug.ug_geeOrig;
	if trial=1;
	sqrt_income=sqrt(SES_income_percap);
	log_income=log(SES_income_percap);
run;

*log transform of income makes for a nice normal covariate;
proc univariate data = onetrial;
	var ageatconsent SES_income_percap sqrt_income log_income;
	histogram;
run;

/*final analysis: 12/14/2012
In conversation with Alex and Kati:
1) exclude ideators (they have the same insensitivity and muddy the waters
2) only include group, fairness, and stake in main GLMM
*/

ods html close;
ods graphics on;
ods pdf file='e:\final_glmm.pdf';
proc glimmix data = ug.ug_geeOrig(where=(Group12467 ne 4)) plots=studentpanel(unpack) order=data method=quad(qpoints=8); *need order data so that contrasts match; *(where=(fairness < 3));
		title 'FINAL UG GLMM: group, stake, fairness.';
		title2 'No Ideators';
		class gender fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        *model accept (event='1') = fairness|stake|Group12467 fairness|ageatconsent_c fairness|stake|gender /solution dist=binary link=logit ddfm=BETWITHIN; * ddfm=kr;
		model accept (event='1') = fairness|stake|Group12467 /solution dist=binary link=logit ddfm=BETWITHIN; * ddfm=kr;
        
		random intercept trial /sub=ID type=VC G;
		nloptions technique=nrridg;
        lsmeans fairness /diff pdiff adjust=tukey plots=meanplot;
		lsmeans stake /diff pdiff adjust=tukey plots=meanplot;
        lsmeans Group12467 /diff pdiff adjust=tukey plots=meanplot;
        *lsmeans stake*Group12467 /diff pdiff adjust=tukey plots=meanplot;
		lsmeans stake*Group12467 /odds oddsratio diff adjust=tukey slice=Group12467 slicediff=Group12467 adjust=tukey plots=meanplot(sliceby=Group12467 join);
		lsmeans fairness*Group12467 /diff pdiff adjust=tukey slice=fairness slicediff=fairness plots=meanplot(sliceby=fairness join);
		format Group12467 grp. stake stake. fairness fairness.;
		*adjust contrasts now that group 4 (ideators) is gone;
		lsmestimate Group12467*stake  'LS hi-lo stk: low vs. high leth' 
			0 0
			0 0
			-1 1
			1 -1; * /cov corr e elsm;

		lsmestimate Group12467*stake  'LS hi-lo stk: ctl vs. high leth' 
			-1 1
			0 0
			0 0
			1 -1; * /cov corr e elsm;

		lsmestimate Group12467*stake  'LS hi-lo stk: ns dep vs. high leth' 
			0 0
			-1 1
			0 0
			1 -1; * /cov corr e elsm;

		lsmestimate Group12467*stake  'LS hi-lo stk: ctl, dep, low leth - high' 
			-.333 .333
			-.333 .333
			-.333 .333
			1 -1 /cov corr e elsm;

run;
ods pdf close;


ods html close;
ods html;
ods graphics on;
ods trace on;

proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=data method=quad(qpoints=8); *need order data so that contrasts match; *(where=(fairness < 3));
        class gender fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        *model accept (event='1') = fairness|stake|Group12467 fairness|ageatconsent_c fairness|stake|gender /solution dist=binary link=logit ddfm=BETWITHIN; * ddfm=kr;
		model accept (event='1') = fairness|stake|Group12467 /solution dist=binary link=logit ddfm=BETWITHIN; * ddfm=kr;
        
		random intercept trial /sub=ID type=VC G;
		nloptions technique=nrridg;
        lsmeans fairness /diff pdiff adjust=tukey plots=meanplot;
		lsmeans stake /diff pdiff adjust=tukey plots=meanplot;
        lsmeans Group12467 /diff pdiff adjust=tukey plots=meanplot;
        lsmeans stake*Group12467 /diff pdiff adjust=tukey plots=meanplot;
		lsmeans stake*Group12467 /odds oddsratio diff adjust=tukey slice=Group12467 slicediff=Group12467 adjust=tukey plots=meanplot(sliceby=Group12467 join);
		lsmeans fairness*Group12467 /diff pdiff adjust=tukey slice=fairness slicediff=fairness plots=meanplot(sliceby=fairness join);
		*output out=glimOut pred=predicted residual=resid pearson=pearson student=student;
        *lsmestimate BlockType -1 3 -1 -1 /e cl divisor=3;  *these estimate ORs > 1, easier to interp;
		format Group12467 grp. stake stake. fairness fairness.;
		lsmestimate Group12467*stake  'LS hi-lo stk: low vs. high leth' 
			0 0
			0 0
			0 0
			-1 1
			1 -1; * /cov corr e elsm;

		lsmestimate Group12467*stake  'LS hi-lo stk: ctl vs. high leth' 
			-1 1
			0 0
			0 0
			0 0
			1 -1; * /cov corr e elsm;

		lsmestimate Group12467*stake  'LS hi-lo stk: ns dep vs. high leth' 
			0 0
			-1 1
			0 0
			0 0
			1 -1; * /cov corr e elsm;

		lsmestimate Group12467*stake  'LS hi-lo stk: ideators vs. high leth' 
			0 0
			0 0
			-1 1
			0 0
			1 -1; * /cov corr e elsm;

		lsmestimate Group12467*stake  'LS hi-lo stk: ctl, dep, low leth - ideator, high' 
			-.333 .333
			-.333 .333
			.5 -.5
			-.333 .333
			.5 -.5 /cov corr e elsm;

run;
ods trace off;







***OLDER STUFF BELOW;
*OLD RSPL APPROACH;
ods html close;
ods html;
ods graphics on;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=formatted; *method=quad; *need order internal to avoid being sorted alphabetically;
        class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 /solution dist=binomial link=logit; * ddfm=kr;
        random _residual_ /sub=ID;* type=cs; *Compound Symmetry of trials within subject;
		nloptions technique=nrridg;
        lsmeans fairness /diff pdiff adjust=tukey plots=meanplot;
		lsmeans stake /diff pdiff adjust=tukey plots=meanplot;
        lsmeans Group12467 /diff pdiff adjust=tukey plots=meanplot;
        lsmeans stake*Group12467 /diff pdiff adjust=tukey plots=meanplot;
		lsmeans stake*Group12467 /odds oddsratio diff adjust=tukey slice=Group12467 slicediff=Group12467 adjust=tukey plots=meanplot(sliceby=Group12467 join);
		*output out=glimOut pred=predicted residual=resid pearson=pearson student=student;
        *lsmestimate BlockType -1 3 -1 -1 /e cl divisor=3;  *these estimate ORs > 1, easier to interp;
		format Group12467 grp. stake stake. fairness fairness.;
		lsmestimate Group12467*stake  'LS hi-lo stk: low vs. high leth' 
			0 0
			0 0
			0 0
			-1 1
			1 -1; * /cov corr e elsm;

		lsmestimate Group12467*stake  'LS hi-lo stk: ctl vs. high leth' 
			-1 1
			0 0
			0 0
			0 0
			1 -1; * /cov corr e elsm;

		lsmestimate Group12467*stake  'LS hi-lo stk: ns dep vs. high leth' 
			0 0
			-1 1
			0 0
			0 0
			1 -1; * /cov corr e elsm;

		lsmestimate Group12467*stake  'LS hi-lo stk: ideators vs. high leth' 
			0 0
			0 0
			-1 1
			0 0
			1 -1; * /cov corr e elsm;

		lsmestimate Group12467*stake  'LS hi-lo stk: ctl, dep, low leth - ideator, high' 
			-.333 .333
			-.333 .333
			.5 -.5
			-.333 .333
			.5 -.5 /cov corr e elsm;

		*estimate 'E hi-lo stk: low vs. high leth' Group12467*stake 
			0 0
			0 0
			0 0
			1 -1
			1 -1;


run;

****TRY TO MIMIC GLMER;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=data method=quad(qpoints=8); *method=quad; *need order internal to avoid being sorted alphabetically;
        class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 /solution dist=binomial link=logit; * ddfm=kr;
        random intercept /sub=ID;* type=cs; *Compound Symmetry of trials within subject;
		nloptions technique=nrridg;
        *lsmeans Group12467 /diff pdiff adjust=tukey plots=meanplot;
        *lsmeans stake*Group12467 /diff pdiff adjust=tukey plots=meanplot;
		*lsmeans stake*Group12467 /odds oddsratio diff adjust=tukey slice=Group12467 slicediff=Group12467 adjust=tukey plots=meanplot(sliceby=Group12467 join);
		*output out=glimOut pred=predicted residual=resid pearson=pearson student=student;
        *lsmestimate BlockType -1 3 -1 -1 /e cl divisor=3;  *these estimate ORs > 1, easier to interp;
		format Group12467 grp. stake stake. fairness fairness.;
		lsmestimate Group12467*stake  'LS hi-lo stk: low vs. high leth' 
			0 0
			0 0
			0 0
			-1 1
			1 -1; * /cov corr e elsm;

		lsmestimate Group12467*stake  'LS hi-lo stk: ctl vs. high leth' 
			-1 1
			0 0
			0 0
			0 0
			1 -1; * /cov corr e elsm;
run;

*test agq approach;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=data method=quad(qpoints=5); *method=quad; *need order internal to avoid being sorted alphabetically;
        class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 /solution dist=binomial link=logit; * ddfm=kr;
        random intercept trial /sub=ID type=cs; *Compound Symmetry of trials within subject;
		nloptions technique=nrridg;
        lsmeans fairness /diff pdiff adjust=tukey plots=meanplot;
		lsmeans stake /diff pdiff adjust=tukey plots=meanplot;
        lsmeans Group12467 /diff pdiff adjust=tukey plots=meanplot;
        lsmeans stake*Group12467 /diff pdiff adjust=tukey plots=meanplot;
		lsmeans stake*Group12467 /odds oddsratio diff adjust=tukey slice=Group12467 slicediff=Group12467 adjust=tukey plots=meanplot(sliceby=Group12467 join);
		*output out=glimOut pred=predicted residual=resid pearson=pearson student=student;
        *lsmestimate BlockType -1 3 -1 -1 /e cl divisor=3;  *these estimate ORs > 1, easier to interp;
		format Group12467 grp. stake stake.;
run;

proc means data = ug.ug_geeOrig;
var iipAmbiv_c;
run;

*add ambivalence;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=data method=rspl; *method=quad; *need order internal to avoid being sorted alphabetically;
        class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 iipAmbiv_c|stake|Group12467 /solution dist=binomial link=logit; * ddfm=kr;
        random _residual_ /sub=ID type=cs; *Compound Symmetry of trials within subject;
		*random intercept /sub=ID type=cs; *Compound Symmetry of trials within subject;
		nloptions technique=nrridg maxiter=1000;
        *lsmeans fairness /diff pdiff adjust=tukey plots=meanplot;
		*lsmeans stake /diff pdiff adjust=tukey plots=meanplot;
        *lsmeans Group12467 /diff pdiff adjust=tukey plots=meanplot;
        *lsmeans stake*Group12467 /diff pdiff adjust=tukey plots=meanplot;
		lsmeans stake*Group12467 /odds oddsratio diff adjust=tukey slice=Group12467 slicediff=Group12467 adjust=tukey plots=meanplot(sliceby=Group12467 join);
		*lsmeans Group12467 /at iipAmbiv_c=-5.024 plots=meanplot(join); *-1sd;
		*lsmeans Group12467 /at iipAmbiv_c=0 plots=meanplot(join); *m;
		*lsmeans Group12467 /at iipAmbiv_c=5.024 plots=meanplot(join); *+1sd;

		output out=glimOut pred=predicted residual=resid pearson=pearson student=student;
        *lsmestimate BlockType -1 3 -1 -1 /e cl divisor=3;  *these estimate ORs > 1, easier to interp;
		format Group12467 grp. stake stake.;

		estimate 'effect of ambivalence in high leth (Ref)' iipAmbiv_c 1;
		estimate 'effect of ambivalence in controls' iipAmbiv_c 1 iipAmbiv_c*Group12467 1 0 0 0 0; * /e;
		estimate 'effect of ambivalence in ns dep ' iipAmbiv_c 1 iipAmbiv_c*Group12467 0 1 0 0 0; * /e;
		estimate 'effect of ambivalence in ideators' iipAmbiv_c 1 iipAmbiv_c*Group12467 0 0 1 0 0; * /e;
		estimate 'effect of ambivalence low leth' iipAmbiv_c 1 iipAmbiv_c*Group12467 0 0 0 1 0; * /e;

		estimate 'ambiv in ctl and low leth vs. ideators and dep' iipAmbiv_c 0 iipAmbiv_c*Group12467 .5 -.5 -.5 .5 0; * /e;


		*lsmestimate Group12467*stake  'LS hi-lo stk: low vs. high leth' 
			0 0
			0 0
			0 0
			-1 1
			1 -1 /cov corr e elsm;

		*lsmestimate Group12467*stake  'LS hi-lo stk: ctl, dep, low leth - ideator, high' 
			-.333 .333
			-.333 .333
			.5 -.5
			-.333 .333
			.5 -.5 /cov corr e elsm;

		*estimate 'E hi-lo stk: low vs. high leth' Group12467*stake 
			0 0
			0 0
			0 0
			1 -1
			1 -1;

run;

proc contents data = glimOut;
run;

*run glimmix for each group to look at effect of ambivalence;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=data; *method=quad; *need order internal to avoid being sorted alphabetically;
		by Group12467;
		class fairness stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake iipAmbiv_c /solution dist=binomial link=logit; * ddfm=kr;
        random _residual_ /sub=ID type=cs; *Compound Symmetry of trials within subject;
		nloptions technique=nrridg maxiter=500;
		format Group12467 grp. stake stake.;
run;

*also add nonplanning impulsivity;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=data method=quad(qpoints=15); *method=quad; *need order internal to avoid being sorted alphabetically;
        class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 iipAmbiv_c|stake|Group12467 BIS_nonplan|Group12467|stake /solution dist=binomial link=logit; * ddfm=kr;
        random intercept /sub=ID type=cs; *Compound Symmetry of trials within subject;
		nloptions technique=nrridg maxiter=500;
        *lsmeans fairness /diff pdiff adjust=tukey plots=meanplot;
		lsmeans stake*Group12467 /odds oddsratio diff adjust=tukey slice=Group12467 slicediff=Group12467 adjust=tukey plots=meanplot(sliceby=Group12467 join);
		format Group12467 grp. stake stake.;
run;

*impulsivity, ;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=data method=quad(qpoints=15); *method=quad; *need order internal to avoid being sorted alphabetically;
        class fairness Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 BIS_nonplan_c|Group12467|stake /solution dist=binomial link=logit; * ddfm=kr;
        random intercept /sub=ID type=cs; *Compound Symmetry of trials within subject;
		nloptions technique=nrridg maxiter=500;
        *lsmeans fairness /diff pdiff adjust=tukey plots=meanplot;
		lsmeans stake*Group12467 /odds oddsratio diff adjust=tukey slice=Group12467 slicediff=Group12467 adjust=tukey plots=meanplot(sliceby=Group12467 join);
		format Group12467 grp. stake stake.;
run;


*look at effects in controls and high lethality only;
data ug_highcont;
	set ug.ug_geeOrig;
	if Group12467 in (1,7);
run;

proc glimmix data = ug_highcont plots=studentpanel(unpack) order=data method=quad(qpoints=15); *method=quad; *need order internal to avoid being sorted alphabetically;
        class Group12467 stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = stake|Group12467 /solution dist=binomial link=logit; * ddfm=kr;
        random intercept /sub=ID type=cs; *Compound Symmetry of trials within subject;
		nloptions technique=nrridg maxiter=500;
		lsmeans stake*Group12467 /odds oddsratio diff adjust=tukey slice=Group12467 slicediff=Group12467 adjust=tukey plots=meanplot(sliceby=Group12467 join);
		format Group12467 grp. stake stake.;
run;



*proc import datafile="e:\ug_gee_covars N129 mark 2.sav" out=ug.ug_geeOrig dbms=sav replace;
*run;

*proc import datafile="e:\ug_gee_covars N129 mark 2.sav" out=ug.ug_geeOrig dbms=sav replace;
*run;

*proc import datafile="e:\ug_gee_covars N129 mark 4.dat" out=ug.ug_geeOrig dbms=TAB replace;
*	getnames=yes;
*run;

/*
On 11/20, I realized that the n=129 dataset from Alex did not match the n=129 dataset from Jan.
After a number of emails, it appears that Jan's 129 (named "mark 4") is the correct 129 dataset.

The code below tries to align the two datasets and identify discrepancies.

proc import datafile="e:\ug_gee_covars N129 mark 4.dta" out=ugUpdates dbms=dta replace;
run;

proc contents data = ugUpdates;
run;

data ugUpdates;
	set ugUpdates;
	keep ID trial Gender SES_income_percap accept_by_stake_ratio;
run;

proc sort data = ug.ug_geeOrig;
	by ID trial;
run;

proc sort data = ugUpdates;
	by ID trial;
run;

data matches nomatch; *ug.ug_geeOrig;
	merge ug.ug_geeOrig (in=full) ugUpdates (in=update);
	by ID trial;
	if full and update then output matches;
	else output nomatch;
run;

*proc print data=nomatch;
*run;
*/


*more conventional CS structure;
*this is a mess because variance is ~0, all variance absorbed in CS term.;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=formatted method=quad(qpoints=1); *need order internal to avoid being sorted alphabetically;
        class fairness Group12467 stake trial; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 /solution dist=binomial link=logit; * ddfm=kr;
        random trial /sub=ID type=CS G GCORR; *Compound Symmetry of trials within subject;
		nloptions technique=QUANEW;*nrridg;
		format Group12467 grp. stake stake. fairness fairness.;
run;

*Toeplitz structure;
proc glimmix data = ug.ug_geeOrig plots=studentpanel(unpack) order=formatted method=quad(qpoints=1); *need order internal to avoid being sorted alphabetically;
        class fairness Group12467 stake trial; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = fairness|stake|Group12467 /solution dist=binomial link=logit; * ddfm=kr;
        random trial /sub=ID type=TOEP G; *Compound Symmetry of trials within subject;
		nloptions technique=QUANEW; *nrridg;
		format Group12467 grp. stake stake. fairness fairness.;
run;

data ugtmp;
	set ug.ug_geeOrig;
	unfair=fairness < 3;
run;

proc glimmix data = ugtmp plots=studentpanel(unpack) order=formatted method=quad(qpoints=8); *laplace;  *need order internal to avoid being sorted alphabetically;
        title 'fairness x stake GLMM';
		class unfair stake; *stake must come last to match the group x stake contrast coding below;
        model accept (event='1') = unfair|stake /solution dist=binary link=logit; * ddfm=kr;
        random intercept trial /sub=ID type=VC G; *cs says to allow intercept and trial to covary;
		nloptions technique=newrap maxiter=200;
run;

