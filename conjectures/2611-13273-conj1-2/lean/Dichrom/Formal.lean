import Dichrom.Marked

namespace Dichrom
open Lean.Grind
attribute [local instance] Semiring.natCast Ring.intCast

/-- The term model of ℤ[X]. Two integer polynomial expressions represent the
same formal polynomial precisely when they are identical under all
interpretations of their generator in commutative rings. -/
def polynomialSetoid : Setoid Poly where
  r p q := ∀ (K : Type) [CommRing K] (x : K), p.eval x = q.eval x
  iseqv := ⟨fun _ _ _ _ => rfl, fun h K _ x => (h K x).symm,
    fun h g K _ x => (h K x).trans (g K x)⟩

def ZPoly := Quotient polynomialSetoid
def Poly.formal (p : Poly) : ZPoly := Quotient.mk polynomialSetoid p

def Poly.subst (p z : Poly) : Poly :=
  match p with
  | .X => z
  | .C a => .C a
  | .add p q => .add (p.subst z) (q.subst z)
  | .mul p q => .mul (p.subst z) (q.subst z)

theorem eval_subst {K : Type} [CommRing K] (x : K) (z p : Poly) :
    (p.subst z).eval x = p.eval (z.eval x) := by
  induction p <;> simp_all [Poly.subst,Poly.eval]

private abbrev X := Poly.X
def xMinusOne : Poly := Poly.add X (.C (-1))
private def sq := Poly.mul X X
private def minus (p q : Poly) := Poly.add p (.mul (.C (-1)) q)

private def sumAt (A : System α) (v : α) (l : List α) (f : List α → List α → Poly) :=
  sumPoly (splits l) (fun (s,r) => if A.ok (v::s) then f s r else .C 0)

private theorem eval_sumAt {K : Type} [CommRing K] (A : System α) (v : α) (l : List α)
    (f : List α → List α → Poly) (x : K) :
    (sumAt A v l f).eval x = splitSum l (fun s r => keep (A.ok (v::s)) ((f s r).eval x)) := by
  unfold sumAt splitSum
  rw [eval_sumPoly]
  apply total_congr; intro ⟨s,r⟩ _
  dsimp only
  cases A.ok (v::s) <;> simp [keep,Poly.eval] <;> grind

private theorem eval_xm {K : Type} [CommRing K] (x : K) : xMinusOne.eval x = x-1 := by
  simp only [xMinusOne,Poly.eval]; grind

private theorem eval_minus {K : Type} [CommRing K] (x : K) (p q : Poly) :
    (minus p q).eval x = p.eval x-q.eval x := by simp only [minus,Poly.eval]; grind

def markedP (A : System α) (v : α) (l : List α) : Poly :=
  .mul X (sumAt A v l (fun _ r => (polynomial A.ok r).subst xMinusOne))

def recursiveH (A : System α) (v : α) (l : List α) : Poly :=
  .mul sq (sumAt A v l (fun _ r => (defect A.ok r).subst xMinusOne))

def weightedP (A : System α) (v : α) (l : List α) : Poly :=
  .mul X (sumAt A v l (fun s r => .mul (minus (.C l.length) (.mul X (.C s.length)))
      ((polynomial A.ok r).subst xMinusOne)))

def forbiddenP (A : System α) (v : α) (l : List α) : Poly :=
  sumPoly (parts A.ok l) (fun p => .mul (falling X p.length) (sumPoly p (fun b =>
    if A.ok (v::b) then .C 0 else minus (.mul X (.C b.length)) (.C l.length))))

private theorem eval_rec {K : Type} [CommRing K] (A : System α) (v : α) (l : List α) (x : K) :
    (recursiveH A v l).eval x = x^2 * splitSum l (fun s r => keep (A.ok (v::s)) (H A.ok r (x-1))) := by
  simp only [recursiveH,sq,X,Poly.eval,eval_sumAt,eval_subst,eval_xm,eval_H]
  grind only

private theorem eval_weight {K : Type} [CommRing K] (A : System α) (v : α) (l : List α) (x : K) :
    (weightedP A v l).eval x = x * splitSum l (fun s r => keep (A.ok (v::s))
      (((l.length:K)-x*(s.length:K))*P A.ok r (x-1))) := by
  simp only [weightedP,X,Poly.eval,eval_sumAt,eval_subst,eval_xm,eval_P,eval_minus,Ring.intCast_natCast]

private theorem eval_forbidden {K : Type} [CommRing K] (A : System α) (v : α) (l : List α) (x : K) :
    (forbiddenP A v l).eval x = correction A v l x := by
  simp only [forbiddenP,correction,partSum,eval_sumPoly,Poly.eval,eval_falling,X]
  apply total_congr; intro p _
  congr 1
  apply total_congr; intro b _
  cases A.ok (v::b) <;> simp [keep,eval_minus,Poly.eval,Ring.intCast_natCast] <;> grind

theorem formal_identity1 (A : System α) (v : α) (l : List α) :
    (polynomial A.ok (v::l)).formal = (markedP A v l).formal := by
  apply Quotient.sound (s:=polynomialSetoid)
  intro K inst x
  simp only [markedP,X,Poly.eval,eval_sumAt,eval_subst,eval_xm,eval_P]
  exact identity1 ..

theorem formal_identity2 (A : System α) (v : α) (l : List α) :
    (Poly.mul xMinusOne (defect A.ok (v::l))).formal =
      (Poly.add (recursiveH A v l) (weightedP A v l)).formal := by
  apply Quotient.sound (s:=polynomialSetoid)
  intro K inst x
  simp only [Poly.eval,eval_xm,eval_H,eval_rec,eval_weight]
  exact identity2 ..

theorem formal_identity3 (A : System α) (v : α) (l : List α) :
    (Poly.mul xMinusOne (defect A.ok (v::l))).formal =
      (Poly.add (recursiveH A v l) (forbiddenP A v l)).formal := by
  apply Quotient.sound (s:=polynomialSetoid)
  intro K inst x
  simp only [Poly.eval,eval_xm,eval_H,eval_rec,eval_forbidden]
  exact identity3 ..

end Dichrom
