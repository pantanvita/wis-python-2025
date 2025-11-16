# test_dna_utils.py
import pytest
from dna_utils import (
    reverse_complement,
    gc_content,
    calculate_tm,
    design_primers,
    calculate_volume,
    theoretical_yield
)

# -----------------------------
# Basic utility tests
# -----------------------------

def test_reverse_complement():
    assert reverse_complement("ATGC") == "GCAT"
    assert reverse_complement("atgc") == "GCAT"

def test_gc_content():
    assert round(gc_content("GGCC"), 1) == 100.0
    assert round(gc_content("AATT"), 1) == 0.0
    assert round(gc_content("ATGC"), 1) == 50.0

def test_calculate_tm():
    # Wallace rule: Tm = 2*(A+T) + 4*(G+C)
    assert calculate_tm("ATGC") == 12  # 2*(A+T=2) + 4*(G+C=2) = 12

def test_calculate_volume():
    assert calculate_volume(10, 1, 20) == 2

def test_theoretical_yield():
    assert theoretical_yield(1, 3) == 8

# -----------------------------
# Primer design tests
# -----------------------------

def test_design_primers_success():
    # Sequence manually chosen to satisfy constraints for primer_length=10
    seq = "ATGCGTACCGTACGTACGTTAGCTAGCTAACCGGTAGCTAGCTA"
    result = design_primers(seq, primer_length=10)
    
    # Check returned dictionary
    assert "forward_primer" in result
    assert "reverse_primer" in result
    
    # GC content and Tm within reasonable range
    assert 40 <= result["f_gc"] <= 60
    assert 40 <= result["r_gc"] <= 60
    assert 55 <= result["f_tm"] <= 65
    assert 55 <= result["r_tm"] <= 65
    assert abs(result["f_tm"] - result["r_tm"]) <= 10

def test_design_primers_failure_short_sequence():
    # Too short sequence should fail
    seq = "ATGCATGCAT"  # 10 nt
    with pytest.raises(ValueError):
        design_primers(seq, primer_length=20)

def test_design_primers_failure_no_possible_primer():
    # Sequence long enough but can't satisfy constraints
    seq = "AAAAAAAACCCCCCCC"  # all A/T or G/C -> Tm mismatch
    with pytest.raises(ValueError):
        design_primers(seq, primer_length=8)
