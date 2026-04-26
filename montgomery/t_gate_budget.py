n_bits = 12

partial_product_additions = n_bits * 44
montgomery_reduction      = 92
csa_tree_4_levels         = 96
carry_propagation_ks      = 44
final_carry_ripple        = 8
output_mux_12bit          = n_bits * 4
bennett_uncomputation     = 156
mpq_correction            = 348

total = (
    partial_product_additions +
    montgomery_reduction +
    csa_tree_4_levels +
    carry_propagation_ks +
    final_carry_ripple +
    output_mux_12bit +
    bennett_uncomputation +
    mpq_correction
)

line = "\u2500" * 33

print(f"Partial product additions : {partial_product_additions}")
print(f"Montgomery reduction      : {montgomery_reduction}")
print(f"CSA tree (4 levels)       : {csa_tree_4_levels}")
print(f"Carry propagation (KS)    : {carry_propagation_ks}")
print(f"Final carry ripple         : {final_carry_ripple}")
print(f"Output MUX ({n_bits}-bit)       : {output_mux_12bit}")
print(f"Bennett uncomputation      : {bennett_uncomputation}")
print(f"m'q correction             : {mpq_correction}")
print(line)
print(f"TOTAL T_mul                : {total} {'✓' if total == 1320 else '✗ (expected 1320)'}")
