# Ray Tracing

The animation shown in the following canvas was written in Rust and
compiled to wasm.

<canvas id="canvas"></canvas>

<script src="./raytracer.js"></script>
<script type="module">
import init, { animate } from "/pkg/raytracer_rs.js";
async function run() {
    await init();

    let cvs = document.getElementById("canvas");
    cvs.width = Math.min(610, window.outerWidth - 40 /*padding*/);
    cvs.height = cvs.width;

    let ctx = cvs.getContext("2d");
    animate(ctx, cvs.width, cvs.height);
}
run();
</script>
