# -*- coding: utf-8 -*-
"""
Internal helper methods for license server client SDK.
Adapted from original Cryptolens implementation for our licensing server.
"""
import base64
import hashlib
import subprocess
import os
import platform
import ssl
import urllib.request
import urllib.parse

def subprocess_args(include_stdout=True):
    """Configure subprocess arguments for cross-platform compatibility."""
    if hasattr(subprocess, 'STARTUPINFO'):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        env = os.environ
    else:
        si = None
        env = None

    if include_stdout:
        ret = {'stdout': subprocess.PIPE}
    else:
        ret = {}

    ret.update({'stdin': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'startupinfo': si,
                'env': env })
    return ret

class LicenseServerHelpers:
    """Helper methods for our license server client SDK."""
    
    @staticmethod
    def get_sha256(string):
        """Compute the SHA256 hash of a string."""
        return hashlib.sha256(string.encode("utf-8")).hexdigest()
    
    @staticmethod
    def i2osp(x, x_len):
        """Integer to Octet String Primitive."""
        if x > (1 << (8 * x_len)):
            return None
        x_rev = []
        for _ in range(0, x_len):
            x, m = divmod(x, 256)
            x_rev.append(m)
        return bytes(reversed(x_rev))
    
    @staticmethod
    def os2ip(x):
        """Octet String to Integer Primitive."""
        import binascii
        h = binascii.hexlify(x)
        return int(h, 16)
       
    @staticmethod
    def rsa_vp1(pair, s):
        """RSA Verification Primitive."""
        n, e = pair
        if s < 0 or n-1 < s:
            return None
        return pow(s, e, n)
    
    @staticmethod
    def emsa_pkcs1_v15_encode(m, em_len, h_len=256):
        """EMSA-PKCS1-v1_5 encoding."""
        h = hashlib.sha256()
        if h_len == 512:
            h = hashlib.sha512()
        h.update(m)
        h_digest = h.digest()

        t = bytes([0x30, 0x31, 0x30, 0x0d, 0x06, 0x09, 0x60, 0x86, 0x48, 0x01, 0x65, 0x03, 0x04, 0x02, 0x01, 0x05, 0x00, 0x04, 0x20]) + h_digest
        if h_len == 512:
            t = bytes([0x30, 0x51, 0x30, 0x0d, 0x06, 0x09, 0x60, 0x86, 0x48, 0x01, 0x65, 0x03, 0x04, 0x02, 0x03, 0x05, 0x00, 0x04, 0x40]) + h_digest
       
        t_len = len(t)
        if em_len < t_len + 11:
            return None
        ps = bytes([0xff for _ in range(em_len - t_len - 3)])
        return b"".join([b"\x00\x01", ps, b"\x00", t])
    
    @staticmethod
    def rsa_assa_pkcs1_v15_verify(pair, m, s, l=256):
        """RSAASSA-PKCS1-v1_5 verification."""
        n, e = pair
        s_int = LicenseServerHelpers.os2ip(s)
        m_int = LicenseServerHelpers.rsa_vp1((n, e), s_int)
        if m_int is None: 
            return False
        em = LicenseServerHelpers.i2osp(m_int, 256)
        if em is None: 
            return False
        em2 = LicenseServerHelpers.emsa_pkcs1_v15_encode(m, 256, l) 
        if em2 is None: 
            return False

        try:
            import hmac
            return hmac.compare_digest(em, em2)
        except (ImportError, AttributeError):
            return em == em2

    @staticmethod
    def verify_signature(response, rsa_public_key):       
        """Verify a signature from .NET RSACryptoServiceProvider."""
        n = LicenseServerHelpers.os2ip(base64.b64decode(rsa_public_key.modulus))
        e = LicenseServerHelpers.os2ip(base64.b64decode(rsa_public_key.exponent))
        
        m = base64.b64decode(response.license_key)
        r = base64.b64decode(response.signature)
        
        return LicenseServerHelpers.rsa_assa_pkcs1_v15_verify((n, e), m, r)
    
    @staticmethod
    def start_process_ps_v2():
        """Get machine UUID using PowerShell v2 method."""
        ps_args = "-Command (Get-CimInstance -Class Win32_ComputerSystemProduct).UUID"
        cmd = ["powershell", *ps_args.split(" ")]  
        
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = proc.communicate(timeout=120)
        
        raw_output = out.decode('utf-8').strip()
        return raw_output
        
    @staticmethod 
    def start_process(command, v=1):
        """Start a subprocess and return output."""
        output = subprocess.check_output(command, **subprocess_args(False))

        if v == 1:
            return output.decode('utf-8')
        elif v == 2:
            raw_output = output.decode('utf-8')
            return raw_output[raw_output.index("UUID")+4:].strip()
        else:
            raise ValueError("Version can be either 1 or 2.")
        
    @staticmethod
    def get_dbus_machine_id():
        """Get machine ID from D-Bus on Linux systems."""
        try:
            with open("/etc/machine-id") as f:
                return f.read().strip()
        except:
            pass
        try:
            with open("/var/lib/dbus/machine-id") as f:
                return f.read().strip()
        except:
            pass
        return ""

    @staticmethod
    def get_inodes():
        """Get inode numbers from system directories on Linux."""
        files = ["/bin", "/etc", "/lib", "/root", "/sbin", "/usr", "/var"]
        inodes = []
        for file in files:
            try:
                inodes.append(os.stat(file).st_ino)
            except: 
                pass
        return "".join([str(x) for x in inodes])

    @staticmethod
    def compute_machine_code():
        """Compute machine code for Linux systems."""
        return LicenseServerHelpers.get_dbus_machine_id() + LicenseServerHelpers.get_inodes()

    @staticmethod
    def read_registry_value(key, subkey, value_name):
        """Read a value from the Windows Registry."""
        try:
            import winreg
            # Open the registry key
            registry_key = winreg.OpenKey(key, subkey, 0, winreg.KEY_READ)
            
            # Query the value
            value, reg_type = winreg.QueryValueEx(registry_key, value_name)
            
            # Close the registry key
            winreg.CloseKey(registry_key)
            
            return value
        
        except FileNotFoundError:
            return None
        except Exception as e:
            return None