#!/bin/bash
echo "running ecdsa tests..."
sage mage/tests/ecdsa_test.sage && \
echo "running ecdsa doctests..." && \
sage -t mage/ecdsa.py && \
echo "running matrix utils tests..." && \
sage mage/tests/matrix_utils_test.sage && \
echo "running matrix utils doctests..." && \
sage -t mage/matrix_utils.py && \
echo "running vector utils doctests..." && \
sage -t mage/vector_utils.py && \
echo "=== TESTS COMPLETE! ==="
