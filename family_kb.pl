% ==========================================
% FAMILY KNOWLEDGE BASE - ASSIGNMENT 2
% RULES ONLY — Facts are added dynamically
% via the data entry module (add_facts.py)
% ==========================================

% ── RULE 1:  Father ──────────────────────
father(X,Y) :- parent(X,Y), male(X).

% ── RULE 2:  Mother ──────────────────────
mother(X,Y) :- parent(X,Y), female(X).

% ── RULE 3:  Son ─────────────────────────
son(X,Y) :- parent(Y,X), male(X).

% ── RULE 4:  Daughter ────────────────────
daughter(X,Y) :- parent(Y,X), female(X).

% ── RULE 5:  Sibling ─────────────────────
sibling(X,Y) :- parent(Z,X), parent(Z,Y).

% ── RULE 6:  Brother ─────────────────────
brother(X,Y) :- sibling(X,Y), male(X).

% ── RULE 7:  Sister ──────────────────────
sister(X,Y) :- sibling(X,Y), female(X).

% ── RULE 8:  Husband ─────────────────────
husband(X,Y) :- married(X,Y), male(X).

% ── RULE 9:  Wife ────────────────────────
wife(X,Y) :- married(X,Y), female(X).
wife(X,Y) :- married(Y,X), female(X).

% ── RULE 10: Spouse ──────────────────────
spouse(X,Y) :- husband(X,Y).
spouse(X,Y) :- wife(X,Y).

% ── RULE 11: Grandfather ─────────────────
grandfather(X,Y) :- parent(X,Z), parent(Z,Y), male(X).

% ── RULE 12: Grandmother ─────────────────
grandmother(X,Y) :- parent(X,Z), parent(Z,Y), female(X).

% ── RULE 13: Grandson ────────────────────
grandson(X,Y) :- grandfather(Y,X), male(X).
grandson(X,Y) :- grandmother(Y,X), male(X).

% ── RULE 14: Granddaughter ───────────────
granddaughter(X,Y) :- grandfather(Y,X), female(X).
granddaughter(X,Y) :- grandmother(Y,X), female(X).

% ── RULE 15: Uncle ───────────────────────
uncle(X,Y) :- parent(Z,Y), brother(X,Z).

% ── RULE 16: Aunt ────────────────────────
aunt(X,Y) :- parent(Z,Y), sister(X,Z).

% ── RULE 17: Nephew ──────────────────────
nephew(X,Y) :- parent(Z,X), sibling(Z,Y), male(X).

% ── RULE 18: Niece ───────────────────────
niece(X,Y) :- parent(Z,X), sibling(Z,Y), female(X).

% ── RULE 19: Cousin ──────────────────────
cousin(X,Y) :- parent(W,X), parent(Z,Y), sibling(W,Z).

% ── RULE 20: Father-in-law ───────────────
father_in_law(X,Y) :- spouse(Y,Z), father(X,Z).

% ── RULE 21: Mother-in-law ───────────────
mother_in_law(X,Y) :- spouse(Y,Z), mother(X,Z).

% ── RULE 22: Son-in-law ──────────────────
son_in_law(X,Y) :- male(X), spouse(X,Z), parent(Y,Z).

% ── RULE 23: Daughter-in-law ─────────────
daughter_in_law(X,Y) :- female(X), spouse(X,Z), parent(Y,Z).

% ── RULE 24: Brother-in-law ──────────────
brother_in_law(X,Y) :- wife(W,Y), brother(X,W).

% ── RULE 25: Sister-in-law ───────────────
sister_in_law(X,Y) :- husband(H,Y), sister(X,H).

% ── RULE 26: Elder Brother ───────────────
elder_brother(X,Y) :- brother(X,Y), older(X,Y).

% ── RULE 27: Younger Brother ─────────────
younger_brother(X,Y) :- brother(X,Y), older(Y,X).

% ── RULE 28: Elder Sister ────────────────
elder_sister(X,Y) :- sister(X,Y), older(X,Y).

% ── RULE 29: Younger Sister ──────────────
younger_sister(X,Y) :- sister(X,Y), older(Y,X).

% ── RULE 30: Taya (elder paternal uncle) ─
taya(X,Y) :- father(F,Y), brother(X,F), older(X,F).

% ── RULE 31: Chacha (younger paternal uncle)
chacha(X,Y) :- father(F,Y), brother(X,F), older(F,X).

% ── RULE 32: Nana (maternal grandfather) ─
nana(X,Y) :- mother(M,Y), father(X,M).

% ── RULE 33: Nani (maternal grandmother) ─
nani(X,Y) :- mother(M,Y), mother(X,M).

% ── RULE 34: Dada (paternal grandfather) ─
dada(X,Y) :- father(F,Y), father(X,F).

% ── RULE 35: Dadi (paternal grandmother) ─
dadi(X,Y) :- father(F,Y), mother(X,F).

% ── RULE 36: Age calculation ─────────────
current_year(2026).
age(P,A) :- dob(P,B), current_year(CY), A is CY-B.

% ── RULE 37: Older comparison ────────────
older(P1,P2) :- age(P1,A1), age(P2,A2), A1 > A2.

% ── RULE 38: Ancestor ────────────────────
ancestor(X,Y) :- parent(X,Y).
ancestor(X,Y) :- parent(X,Z), ancestor(Z,Y).

% ── RULE 39: Descendant ──────────────────
descendant(X,Y) :- ancestor(Y,X).

% ── RULE 40: Related ─────────────────────
related(X,Y) :- ancestor(X,Y).
related(X,Y) :- ancestor(Y,X).
related(X,Y) :- spouse(X,Y).

% ==========================================
% DYNAMICALLY ADDED FACTS WILL APPEAR BELOW
female(fatima).  % added 2026-06-22 20:23:51
female(samina).  % added 2026-06-22 20:23:43
male(sattar).  % added 2026-06-22 20:23:36
male(hamza).  % added 2026-06-22 20:23:29
male(ali).  % added 2026-06-22 20:23:25
dob(ayesha,2005).  % added 2026-06-22 20:19:27
dob(yousaf,2001).  % added 2026-06-22 20:19:27
dob(maryam,2003).  % added 2026-06-22 20:19:27
dob(awais,2007).  % added 2026-06-22 20:19:27
dob(shaista,1980).  % added 2026-06-22 20:19:27
dob(samina,1982).  % added 2026-06-22 20:19:27
dob(nasir,1978).  % added 2026-06-22 20:19:27
dob(qalsoom,1950).  % added 2026-06-22 20:19:27
dob(sattar,1945).  % added 2026-06-22 20:19:27
dob(zain,2015).  % added 2026-06-22 20:19:27
dob(alia,2010).  % added 2026-06-22 20:19:27
dob(hamza,2005).  % added 2026-06-22 20:19:27
dob(usman,1985).  % added 2026-06-22 20:19:27
dob(fatima,1982).  % added 2026-06-22 20:19:27
dob(ali,1980).  % added 2026-06-22 20:19:27
dob(kamran,1975).  % added 2026-06-22 20:19:27
dob(sara,1955).  % added 2026-06-22 20:19:27
dob(tariq,1950).  % added 2026-06-22 20:19:27
married(kamran,zara).  % added 2026-06-22 20:19:27
married(saqib,shehnaz).  % added 2026-06-22 20:19:27
married(akhtar,suriya).  % added 2026-06-22 20:19:27
married(sattar,qalsoom).  % added 2026-06-22 20:19:27
married(nasir,shaista).  % added 2026-06-22 20:19:27
married(ali,samina).  % added 2026-06-22 20:19:27
married(ali,fatima).  % added 2026-06-22 20:19:27
married(tariq,sara).  % added 2026-06-22 20:19:27
parent(fatima,zain).  % added 2026-06-22 20:19:27
parent(fatima,alia).  % added 2026-06-22 20:19:27
parent(fatima,hamza).  % added 2026-06-22 20:19:27
parent(ali,zain).  % added 2026-06-22 20:19:27
parent(ali,alia).  % added 2026-06-22 20:19:27
parent(ali,hamza).  % added 2026-06-22 20:19:27
parent(tariq,usman).  % added 2026-06-22 20:19:27
parent(tariq,kamran).  % added 2026-06-22 20:19:27
parent(qalsoom,zara).  % added 2026-06-22 20:19:27
parent(sattar,zara).  % added 2026-06-22 20:19:27
parent(kamran,mehnaz).  % added 2026-06-22 20:19:27
parent(zara,mehnaz).  % added 2026-06-22 20:19:27
parent(shehnaz,shaista).  % added 2026-06-22 20:19:27
parent(saqib,shaista).  % added 2026-06-22 20:19:27
parent(suriya,samina).  % added 2026-06-22 20:19:27
parent(akhtar,samina).  % added 2026-06-22 20:19:27
parent(qalsoom,nasir).  % added 2026-06-22 20:19:27
parent(qalsoom,ali).  % added 2026-06-22 20:19:27
parent(sattar,nasir).  % added 2026-06-22 20:19:27
parent(sattar,ali).  % added 2026-06-22 20:19:27
parent(shaista,ayesha).  % added 2026-06-22 20:19:27
parent(shaista,yousaf).  % added 2026-06-22 20:19:27
parent(nasir,ayesha).  % added 2026-06-22 20:19:27
parent(nasir,yousaf).  % added 2026-06-22 20:19:27
parent(samina,awais).  % added 2026-06-22 20:19:27
parent(samina,maryam).  % added 2026-06-22 20:19:27
parent(ali,awais).  % added 2026-06-22 20:19:27
parent(ali,maryam).  % added 2026-06-22 20:19:27
female(alia).  % added 2026-06-22 20:19:27
female(fatima).  % added 2026-06-22 20:19:27
female(sara).  % added 2026-06-22 20:19:27
female(mehnaz).  % added 2026-06-22 20:19:27
female(zara).  % added 2026-06-22 20:19:27
female(shehnaz).  % added 2026-06-22 20:19:27
female(suriya).  % added 2026-06-22 20:19:27
female(qalsoom).  % added 2026-06-22 20:19:27
female(ayesha).  % added 2026-06-22 20:19:27
female(maryam).  % added 2026-06-22 20:19:27
female(shaista).  % added 2026-06-22 20:19:27
female(samina).  % added 2026-06-22 20:19:27
male(tariq).  % added 2026-06-22 20:19:27
male(usman).  % added 2026-06-22 20:19:27
male(zain).  % added 2026-06-22 20:19:27
male(hamza).  % added 2026-06-22 20:19:27
male(kamran).  % added 2026-06-22 20:19:27
male(saqib).  % added 2026-06-22 20:19:27
male(akhtar).  % added 2026-06-22 20:19:27
male(sattar).  % added 2026-06-22 20:19:27
male(yousaf).  % added 2026-06-22 20:19:27
male(awais).  % added 2026-06-22 20:19:27
male(nasir).  % added 2026-06-22 20:19:27
male(ali).  % added 2026-06-22 20:19:27
married(samina,ali).  % added 2026-06-22 20:19:11
married(fatima,ali).  % added 2026-06-22 20:18:56
parent(ali,hamza).  % added 2026-06-22 20:18:06
male(hamza).  % added 2026-06-22 20:17:44
female(sara).  % added 2026-06-22 20:17:29
male(ali).  % added 2026-06-22 20:17:22
