import cx_Freeze

executables = [cx_Freeze.Executable("pong.py")]

cx_Freeze.setup(
    name="Pong",
    options={"build_exe": {
                    "packages":
                        ["pygame"],
                        "include_files":[
                            "assets/pong-bg.png",
                            'assets/ball.png',
                            'assets/paddle.png',
                            'assets/sound-on-img.png',
                            'assets/sound-off-img.png',
                            'assets/Monkeys-Spinning-Monkeys.mp3',
                            "assets/paddle1-hit-ball.mp3",
                            "assets/paddle2-hit-ball.mp3",
                            "assets/hit.mp3",
                            "assets/ball-bounce.mp3"
                        ]
                }
            },
    executables = executables

)