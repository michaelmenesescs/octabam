"""michael -- the rig plus octatrick, USB AUDIO EXTENDED, Octakit and the fixes.

bottleservice's selection (the bus, three stations, hosts, TEMPO SYNC, CC MAP,
MODE DEFAULTS, SCENES P2, Octakit with its bridges) without TEMPO BUS, which
shares the second free gap with SYNTH MACHINE; Tim Hastie's SYNTH MACHINE,
SCALE QUANTIZER and DIRECT JUMP; USB MIDI and USB AUDIO EXTENDED (20
channels, as octatrick-usb); REPITCH; the recorder fixes (as recfix); the
LO-FI AMF fix; TAPE ECHO and EUCLID. For an Octatrack MKI.
"""

from remix.schema import Proof, Remix

REMIX = Remix(
    name="michael",
    family="rig", proof=Proof.CHECK, proof_note="unbuilt",
    doc="The rig + octatrick + USB AUDIO EXTENDED + Octakit + REPITCH + recorder fixes + TAPE ECHO + EUCLID.",
    modules=("REVERB SERVER", "DELAY SERVER", "SEND",
             "SPECTRUM", "CHARACTER", "MODULATION",
             "TAPE ECHO", "EUCLID",
             "TEMPO SYNC", "CC MAP", "MODE DEFAULTS", "RIG HOSTS",
             "DIRECT JUMP", "SYNTH MACHINE",
             "USB MIDI", "USB AUDIO EXTENDED",
             "OCTAKIT", "SCENES KITS",
             "SCENES P2", "SCENES P2 KITS",
             "REPITCH",
             "FLEX SEEK BIND", "FLEX SEEK BIND CTR", "RECORDER SPACING",
             "RECORDER HOLD", "RLEN PLEN",
             "LOFI AMF FIX"),
    fallback="SEND",
    hidden=("REVERB SERVER", "DELAY SERVER"),
    host_slots=(("DELAY SERVER", 2), ("REVERB SERVER", 2)),
    locked=("REVERB SERVER", "DELAY SERVER"),
    fx1=("SPECTRUM", "CHARACTER", "MODULATION", "EUCLID"),
)
