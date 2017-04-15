#!/bin/bash
echo "running ecdsa tests..."
sage mage/tests/ecdsa_test.sage
echo "running matrix utils tests..."
sage mage/tests/matrix_utils_test.sage
