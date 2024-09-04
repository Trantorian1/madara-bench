# ============================================================================ #
#                         STARKNET NODE BENCHMAR RUNNER                        #
# ============================================================================ #

MADARA = ./madara

define with_context
	nix develop $(1) \
		--extra-experimental-features "nix-command flakes" \
		--command sh -c "cd $(1)/node && $(2)"
endef

.PHONY: all
all:
	@echo TODO

.PHONY: madara
madara:
	$(call with_context, $(MADARA), cargo run --release -- \
    	--name madara                                      \
    	--base-path ../madara-db                           \
    	--network main                                     \
    	--l1-endpoint ${ETHEREUM_API_URL}                  \
    	--gateway-key ${GATEWAY_KEY}                       \
	)

.PHONY: clean
clean:
	$(call with_context, $(MADARA), cargo clean)
