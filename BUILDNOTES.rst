==============================================================================
Build Issues with Travis
==============================================================================

Issue
^^^^^

While the test ran locally without issues, Travis did not accept the configuration of the project.

It is puzzling as the standard project layout was utilized.

The pytest.ini is fairly standard: ::

    [pytest]
    addopts =
        --cov=csci_2019_project
        --cov-branch
        --pyargs
    testpaths = csci_2019_project
    DJANGO_SETTINGS_MODULE=config.settings.test



The tests are in the folder ./csci_2019_project/users/tests. This was provided by the Django cookiecutter template.

All the __init__.py files were accounted for, to enable the proper import statements.

The Travis logs shows this::

    $ python -m pytest --cov-report xml --cov-report term
    ============================= test session starts ==============================
    platform linux -- Python 3.7.1, pytest-4.6.7, py-1.8.0, pluggy-0.13.1
    Django settings: config.settings.test (from ini file)
    rootdir: /home/travis/build/dliu936/csci_2019_project, inifile: pytest.ini, testpaths: csci_2019_project
    plugins: cov-2.8.1, cookies-0.4.0, django-3.7.0
    collected 0 items / 5 errors
    ==================================== ERRORS ====================================
    _________ ERROR collecting csci_2019_project/users/tests/test_forms.py _________
    ImportError while importing test module '/home/travis/build/dliu936/csci_2019_project/csci_2019_project/users/tests/test_forms.py'.
    Hint: make sure your test modules/packages have valid Python names.
    Traceback:
    ModuleNotFoundError: No module named 'csci_2019_project.csci_2019_project'


The error that the module 'csci_2019_project.csci_2019_project' could not be found implies that it is trying to import
like so: 'from csci_2019_project.csci_2019_project ... ' or 'import csci_2019_project.csci_2019_project ...'.

It is not obvious what the real issue is.  Many hours were devoted to find a resolution but none worked.

Among the attempted to solutions were:

#. Moving the tests to the root folder.
#. Using python -m pytest to run on the sys.path
#. Moving and removing the conftest.py and __init__.py from the root folder csc1_2019_project/
#. Forcing conftest.py to use the current working directory using:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#. Various settings in pytest.ini to force the root folder to be /csci_2019_project/csci_2019_project


All the paths on Travis were correct, however it is unknown why it is trying to import an extraneous module that is not
specified anywhere in the code. What made it more difficult to understand is why it runs fine on a local instance without
any issues.


The output from a local test run::

    $ pytest
    ============================================================================================== test session starts ==============================================================================================
    platform win32 -- Python 3.7.4, pytest-4.6.7, py-1.8.0, pluggy-0.13.1
    Django settings: config.settings.test (from ini file)
    rootdir: D:\advpython\csciproject\csci2019project, inifile: pytest.ini, testpaths: csci_2019_project
    plugins: cookies-0.4.0, cov-2.8.1, django-3.7.0
    collected 14 items

    csci_2019_project\users\tests\test_forms.py .                                                                                                                                                              [  7%]
    csci_2019_project\users\tests\test_models.py .                                                                                                                                                             [ 14%]
    csci_2019_project\users\tests\test_project.py ......                                                                                                                                                       [ 57%]
    csci_2019_project\users\tests\test_urls.py ...                                                                                                                                                             [ 78%]
    csci_2019_project\users\tests\test_views.py ...

    ...

    ----------- coverage: platform win32, python 3.7.4-final-0 -----------
    Name                                                                          Stmts   Miss Branch BrPart  Cover
    ---------------------------------------------------------------------------------------------------------------
    csci_2019_project\__init__.py                                                     0      0      0      0   100%
    csci_2019_project\contrib\__init__.py                                             0      0      0      0   100%
    csci_2019_project\contrib\sites\__init__.py                                       0      0      0      0   100%
    csci_2019_project\contrib\sites\migrations\0001_initial.py                        6      0      0      0   100%
    csci_2019_project\contrib\sites\migrations\0002_alter_domain_unique.py            5      0      0      0   100%
    csci_2019_project\contrib\sites\migrations\0003_set_site_domain_and_name.py      11      2      0      0    82%
    csci_2019_project\contrib\sites\migrations\__init__.py                            0      0      0      0   100%
    csci_2019_project\reports\__init__.py                                             0      0      0      0   100%
    csci_2019_project\reports\apps.py                                                10      0      0      0   100%
    csci_2019_project\reports\models.py                                               0      0      0      0   100%
    csci_2019_project\reports\urls.py                                                 3      0      0      0   100%
    csci_2019_project\reports\views.py                                              138     77     20      0    39%
    csci_2019_project\users\__init__.py                                               0      0      0      0   100%
    csci_2019_project\users\adapters.py                                              11     11      0      0     0%
    csci_2019_project\users\admin.py                                                 12      0      2      0   100%
    csci_2019_project\users\apps.py                                                  10      0      0      0   100%
    csci_2019_project\users\forms.py                                                 18      0      0      0   100%
    csci_2019_project\users\migrations\0001_initial.py                                8      0      0      0   100%
    csci_2019_project\users\migrations\__init__.py                                    0      0      0      0   100%
    csci_2019_project\users\models.py                                                 8      0      0      0   100%
    csci_2019_project\users\tests\__init__.py                                         0      0      0      0   100%
    csci_2019_project\users\tests\factories.py                                       14      0      0      0   100%
    csci_2019_project\users\urls.py                                                   4      0      0      0   100%
    csci_2019_project\users\views.py                                                 28      2      0      0    93%
    csci_2019_project\utils\__init__.py                                               0      0      0      0   100%
    csci_2019_project\utils\context_processors.py                                     3      0      0      0   100%
    ---------------------------------------------------------------------------------------------------------------
    TOTAL                                                                           289     92     22      0    64%

    ==================================================================================== 14 passed, 40 warnings in 65.76 seconds ====================================================================================


