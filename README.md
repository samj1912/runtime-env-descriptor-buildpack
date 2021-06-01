# Runtime Environment Descriptor Buildpack

![Version](https://img.shields.io/badge/dynamic/json?url=https://cnb-registry-api.herokuapp.com/api/v1/buildpacks/sam/runtime-env-descriptor&label=Version&query=$.latest.version)

This is a [Cloud Native Buildpack](https://buildpacks.io) that configures runtime environment variables using a [project descriptor](https://github.com/buildpacks/spec/blob/main/extensions/project-descriptor.md#project-descriptor) file - `project.toml`

## Usage

The buildpack automatically sets runtime env vars when you run a build:

```bash
pack build --buildpack sam/runtime-end-descriptor myapp
```

You can customize the runtime environment variables configuration by creating a `project.toml` file in your application, and a table like:

```toml
[[io.buildpacks.run.env]]
name = "<env-var-name>"
value = "<env-var-value>"
# This key is optional and defaults to "default"
# For a list of behaviors check out - https://github.com/buildpacks/spec/blob/main/buildpack.md#environment-variable-modification-rules
# Supported behaviors are "default", "append", "prepend" and "override"
behaviour = "<env-var-behavior"
# The delimiter to use in case the behavior is "append" or "prepend".
# This key is ignored if the behavior is "default" or "override".
# If this key is not provided and the behavior is "prepend" or "append"
# A default value of ":" is used.
delimiter = "<env-var-delimiter>"

# You can also set env vars for specific processes
[[io.buildpacks.run.process-env.<process-type>]]
name = "<env-var-name>"
value = "<env-var-value>"
# This key is optional and defaults to "default"
# For a list of behaviors check out - https://github.com/buildpacks/spec/blob/main/buildpack.md#environment-variable-modification-rules
# Supported behaviors are "default", "append", "prepend" and "override"
behaviour = "<env-var-behavior"
# The delimiter to use in case the behavior is "append" or "prepend".
# This key is ignored if the behavior is "default" or "override".
# If this key is not provided and the behavior is "prepend" or "append"
# A default value of ":" is used.
delimiter = "<env-var-delimiter>"
```

## Example

For example create a `project.toml` file with the following content - 

```toml
[[io.buildpacks.run.env]]
name = "test"
value = "test"
behavior = "override"

[[io.buildpacks.run.process-env.test]]
name = "test"
value = "test"
behavior = "override"

[[io.buildpacks.run.process-env.test]]
name = "test"
value = "test"
behavior = "prepend"

[[io.buildpacks.run.process-env.test-another]]
name = "test"
value = "test"
behavior = "append"
delimiter = ";"
```

Then run - 

```bash
pack build --buildpack sam/runtime-env-descriptor myapp
docker run --entrypoint another-echo -e MYVAR=hello myapp
```

