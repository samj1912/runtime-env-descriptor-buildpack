from typing import Any, Dict
import libcnb
import toml

DEFAULT_BEHAVIOR = "default"
DEFAULT_DELIMITER = ":"


def detector(context: libcnb.DetectContext) -> libcnb.DetectResult:
    project_descriptor = context.application_dir / "project.toml"
    result = libcnb.DetectResult()
    if project_descriptor.exists() and (
        toml.load(context.application_dir / "project.toml")
        .get("io", {})
        .get("buildpacks", {})
        .get("run", {})
    ):
        result.passed = True
    return result


def builder(context: libcnb.BuildContext) -> libcnb.BuildResult:
    print("Running Runtime Environment Descriptor Buildpack")
    project_descriptor = toml.load(context.application_dir / "project.toml")["io"][
        "buildpacks"
    ]["run"]
    layer = context.layers.get("env-vars")
    layer.reset()
    layer.launch = True
    result = libcnb.BuildResult()
    result.layers.append(layer)
    _set_env_vars(
        project_descriptor.get("env", []),
        layer.launch_env,
    )
    print(f"Set launch environment to {layer.launch_env}")
    process_types = project_descriptor.get("process-env", {})
    for process_type, process_env in process_types.items():
        _set_env_vars(
            process_env,
            layer.process_launch_envs.setdefault(process_type, libcnb.Environment()),
        )
        print(
            f"Set process launch environment for process {process_type} to {layer.process_launch_envs[process_type]}"
        )
    return result


def _set_env_vars(env_table: Dict[str, Any], env: libcnb.Environment):
    for env_var in env_table:
        behavior = env_var.get("behavior", DEFAULT_BEHAVIOR)
        if behavior in {"default", "override"}:
            getattr(env, behavior)(env_var["name"], env_var["value"])
        elif behavior in {"prepend", "append"}:
            getattr(env, behavior)(
                env_var["name"],
                env_var["value"],
                env_var.get("delimiter", DEFAULT_DELIMITER),
            )
        else:
            raise ValueError(f"Invalid behavior type {behavior}")


if __name__ == "__main__":
    libcnb.run(detector=detector, builder=builder)
