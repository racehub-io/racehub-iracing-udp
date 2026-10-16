from racehub_iracing_udp import __version__


def generate_version_file():
    product_name = "racehub_iracing_udp"

    # convert string version into tuple
    version_tuple = tuple(map(int, __version__.split("."))) + (
        0,
    )  # assuming it's in 'x.y.z' format

    # for product_name in product_names:
    with open(f"racehub_iracing_udp/{product_name.lower()}_version.txt", "w") as f:
        f.write(
            f"""VSVersionInfo(
ffi=FixedFileInfo(
    filevers={version_tuple},
    prodvers={version_tuple},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
),
kids=[
    StringFileInfo(
    [
        StringTable(
        '040904B0',
        [
            StringStruct('CompanyName', 'RaceHub'),
            StringStruct('FileDescription', '{product_name}'),
            StringStruct('FileVersion', '{__version__}'),
            StringStruct('InternalName', '{product_name}'),
            StringStruct('ProductName', '{product_name}'),
            StringStruct('ProductVersion', '{__version__}')
        ]
        )
    ]
    ),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
]
)"""
        )
