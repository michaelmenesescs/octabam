"""michael-rig -- candidate: the rig + synth + direct jump + USB AUDIO EXTENDED + Octakit."""
from remix.schema import Proof, Remix
REMIX = Remix(
    name="michael-rig", family="rig", proof=Proof.CHECK, proof_note="candidate",
    doc="Candidate: the rig + SYNTH + DIRECT JUMP + USB AUDIO EXTENDED + Octakit.",
    modules=("REVERB SERVER", "DELAY SERVER", "SEND",
             "SPECTRUM", "CHARACTER", "MODULATION",
             "TEMPO SYNC", "MODE DEFAULTS", "RIG HOSTS",
             "DIRECT JUMP", "SYNTH MACHINE",
             "USB MIDI", "USB AUDIO EXTENDED",
             "OCTAKIT", "SCENES P2", "SCENES P2 KITS",
             "LOFI AMF FIX"),
    fallback="SEND",
    hidden=("REVERB SERVER", "DELAY SERVER"),
    host_slots=(("DELAY SERVER", 2), ("REVERB SERVER", 2)),
    locked=("REVERB SERVER", "DELAY SERVER"),
    fx1=("SPECTRUM", "CHARACTER", "MODULATION"),
)
