.PHONY: help test package clean

help:
	@echo "Targets:"
	@echo "  make test     - Run mechanical test suite for unwind-preview.py"
	@echo "  make package  - Build .skill bundle for distribution"
	@echo "  make clean    - Remove generated artifacts"

test:
	python3 scripts/test_unwind_preview.py

package:
	python3 scripts/package_skill.py .
	@echo ""
	@echo "Install via: npx skills add <repo> -g -a claude-code -a gemini-cli -a codex -a pi -y"

clean:
	rm -f karpathy-wiki-skill.skill
	find . -name __pycache__ -type d -exec rm -rf {} +
	find . -name '*.pyc' -delete
