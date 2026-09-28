"""michael-perf -- candidate: octatrick-usb + Octakit + REPITCH + TAPE ECHO + LO-FI fix, stock effects."""
from remix.schema import Proof, Remix
REMIX = Remix(
    name="michael-perf", family="mods", proof=Proof.CHECK, proof_note="candidate",
    doc="Candidate: octatrick-usb + Octakit + REPITCH + TAPE ECHO + LO-FI fix on the stock effects.",
    modules=("DIRECT JUMP", "SCALE QUANTIZER", "SYNTH MACHINE",
             "USB MIDI", "USB AUDIO EXTENDED", "OCTAKIT",
             "REPITCH", "LOFI AMF FIX",
             "FILTER", "EQUALIZER", "DJ EQ", "PHASER", "FLANGER", "CHORUS",
             "SPATIALIZER", "COMB FILTER", "COMPRESSOR", "LO-FI", "DELAY",
             "PLATE REV", "SPRING REV", "DARK REV"),
    fallback="NONE",
)
