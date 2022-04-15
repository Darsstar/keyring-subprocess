try:
    import keyring
except ImportError:
    import sys
    from ._loader import KeyringSubprocessFinder

    sys.meta_path.append(KeyringSubprocessFinder())
