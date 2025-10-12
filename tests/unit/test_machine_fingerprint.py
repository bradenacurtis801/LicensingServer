"""
Unit tests for machine fingerprinting.
No database or server required.
"""
import pytest
from client_sdk.utils.machine_fingerprint import MachineFingerprint


@pytest.mark.unit
class TestMachineFingerprint:

    def test_generates_non_empty_fingerprint(self):
        fingerprint = MachineFingerprint.generate_fingerprint()
        assert fingerprint is not None
        assert len(fingerprint) > 0

    def test_fingerprint_is_string(self):
        assert isinstance(MachineFingerprint.generate_fingerprint(), str)

    def test_fingerprint_is_consistent(self):
        fp1 = MachineFingerprint.generate_fingerprint()
        fp2 = MachineFingerprint.generate_fingerprint()
        assert fp1 == fp2
