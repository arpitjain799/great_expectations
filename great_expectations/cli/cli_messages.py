from great_expectations.data_context.data_context.file_data_context import (
    FileDataContext,
)

GREETING = r"""<cyan>
  ___              _     ___                  _        _   _
 / __|_ _ ___ __ _| |_  | __|_ ___ __  ___ __| |_ __ _| |_(_)___ _ _  ___
| (_ | '_/ -_) _` |  _| | _|\ \ / '_ \/ -_) _|  _/ _` |  _| / _ \ ' \(_-<
 \___|_| \___\__,_|\__| |___/_\_\ .__/\___\__|\__\__,_|\__|_\___/_||_/__/
                                |_|
             ~ Always know what to expect from your data ~
</cyan>"""

LETS_BEGIN_PROMPT = """Let's create a new Data Context to hold your project configuration.

Great Expectations will create a new directory with the following structure:

    great_expectations
    |-- great_expectations.yml
    |-- expectations
    |-- checkpoints
    |-- plugins
    |-- .gitignore
    |-- uncommitted
        |-- config_variables.yml
        |-- data_docs
        |-- validations

OK to proceed?"""

PROJECT_IS_COMPLETE = "This looks like an existing project that <green>appears complete!</green> You are <green>ready to roll.</green>\n"

RUN_INIT_AGAIN = (
    "OK. You must run <green>great_expectations init</green> to fix the missing files!"
)

COMPLETE_ONBOARDING_PROMPT = """
It looks like you have a partially initialized Great Expectations project. Would you like to fix this automatically by adding the following missing files (existing files will not be modified)?

   great_expectations
    |-- plugins
    |-- uncommitted
"""

ONBOARDING_COMPLETE = """
Great Expectations added some missing files required to run.
  - You may see new files in `<yellow>great_expectations/uncommitted</yellow>`.
  - You may need to add secrets to `<yellow>great_expectations/uncommitted/config_variables.yml</yellow>` to finish onboarding.
"""

READY_FOR_CUSTOMIZATION = """<cyan>Congratulations! You are now ready to customize your Great Expectations configuration.</cyan>"""

HOW_TO_CUSTOMIZE = f"""\n<cyan>You can customize your configuration in many ways. Here are some examples:</cyan>

  <cyan>Use the CLI to:</cyan>
    - Run `<green>great_expectations datasource new</green>` to connect to your data.
    - Run `<green>great_expectations checkpoint new <checkpoint_name></green>` to bundle data with Expectation Suite(s) in a Checkpoint for later re-validation.
    - Run `<green>great_expectations suite --help</green>` to create, edit, list, profile Expectation Suites.
    - Run `<green>great_expectations docs --help</green>` to build and manage Data Docs sites.

  <cyan>Edit your configuration in {FileDataContext.GX_YML} to:</cyan>
    - Move Stores to the cloud
    - Add Slack notifications, PagerDuty alerts, etc.
    - Customize your Data Docs

<cyan>Please see our documentation for more configuration options!</cyan>
"""

SECTION_SEPARATOR = "\n================================================================================\n"

FLUENT_DATASOURCE_LIST_WARNING = """We've detected that you have at least one fluent style Datasource in your Data Context. Fluent style Datasources cannot be listed via the CLI.
If you would like to see a list of your fluent style Datasources, you can run the following code:

context = gx.get_context()
context.list_datasources()

Please see the following doc for more information: https://docs.greatexpectations.io/docs/reference/api/data_context/AbstractDataContext_class#great_expectations.data_context.AbstractDataContext.list_datasources
"""

FLUENT_DATASOURCE_DELETE_ERROR = """Fluent style Datasources can not be deleted via the CLI.
If you would like to delete a fluent style Datasource, you can run the following code:

context = gx.get_context()
context.delete_datasource(datasource_name)

Please see the following doc for more information: https://docs.greatexpectations.io/docs/reference/api/data_context/AbstractDataContext_class#great_expectations.data_context.AbstractDataContext.delete_datasource
"""
