import time
import os
import sys
from hashlib import sha256
from secrets import token_hex
from chiapos import DiskPlotter, DiskProver
from blspy import PrivateKey, PrependSignature
from src.types.sized_bytes import bytes32
from src.types.full_block import FullBlock
from src.types.trunk_block import TrunkBlock
from src.types.block_body import BlockBody
from src.types.challenge import Challenge
from src.types.block_header import BlockHeader, BlockHeaderData
from src.types.proof_of_space import ProofOfSpace
from src.types.proof_of_time import ProofOfTime, ProofOfTimeOutput
from src.types.classgroup import ClassgroupElement
from src.consensus import constants, pot_iterations, block_rewards
from src.util.ints import uint64, uint32, uint8
from src.types.coinbase import CoinbaseInfo
from src.types.fees_target import FeesTarget
from lib.chiavdf.inkfish.create_discriminant import create_discriminant
from lib.chiavdf.inkfish.classgroup import ClassGroup
from lib.chiavdf.inkfish.proof_of_time import create_proof_of_time_nwesolowski


# Use the empty string as the seed for the private key
sk: PrivateKey = PrivateKey.from_seed(b'')
pool_pk = sk.get_public_key()
plot_pk = sk.get_public_key()
coinbase_target = sha256(sk.get_public_key().serialize()).digest()
fee_target = sha256(sk.get_public_key().serialize()).digest()
k = 19
n_wesolowski = 3

genesis_block_hardcoded = b'\x15N3\xd3\xf9H\xc2K\x96\xfe\xf2f\xa2\xbf\x87\x0e\x0f,\xd0\xd4\x0f6s\xb1".\\\xf5\x8a\xb4\x03\x84\x8e\xf9\xbb\xa1\xca\xdef3:\xe4?\x0c\xe5\xc6\x12\x80\x15N3\xd3\xf9H\xc2K\x96\xfe\xf2f\xa2\xbf\x87\x0e\x0f,\xd0\xd4\x0f6s\xb1".\\\xf5\x8a\xb4\x03\x84\x8e\xf9\xbb\xa1\xca\xdef3:\xe4?\x0c\xe5\xc6\x12\x80\x13\x00\x00\x00\x98\xf9\xeb\x86\x90Kj\x01\x1cZk_\xe1\x9c\x03;Z\xb9V\xe2\xe8\xa5\xc8\n\x0c\xbbU\xa6\xc5\xc5\xbcH\xa3\xb3fd\xcd\xb8\x83\t\xa9\x97\x96\xb5\x91G \xb2\x9e\x05\\\x91\xe1<\xee\xb1\x06\xc3\x18~XuI\xc8\x8a\xb5b\xd7.7\x96Ej\xf3DThs\x18s\xa5\xd4C\x1ea\xfd\xd5\xcf\xb9o\x18\xea6n\xe22*\xb0]%\x15\xd0i\x83\xcb\x9a\xa2.+\x0f1\xcd\x03Z\xf3]\'\xbf|\x8b\xa6\xbcF\x10\xe8Q\x19\xaeZ~\xe5\x1f\xf1)\xa3\xfb\x82\x1a\xb8\x12\xce\x19\xc8\xde\xb9n\x08[\xef\xfd\xf9\x0c\xec\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\'\x8c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07~\xccf\x88\xef\xc8z;\xc9\x99\xdaSO\xa2\xdbC\x84\xe1\x9d\xc9Iv\xdbH\xb4\x9fiI\x1ew\xa78Gu\xe0\x9bg\xfdtBU\xfa\xe8\x9f\x13A\xb76iVx\xadU~\x8bj^\xeaV\xfd@\xdf,\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xedVsY\xdf\xa18.\x050\x90\x9c\xb3\xed\xaa\xb0Kv\x81{\x9a\xce=\xed\xc2\xc9m/\xce\x9b[\x04M\xbb\xe8\xdeCNg\xb6<n~o[\x99\xbb\x11\x8d\x11pL\x0f\x1b\x1b\xf9\x94\x06\xd0+1\xfa\xc1\x03\x00\x00\x03\x8e\x00,\x90H!\xf9\x89\x1d\x1b\xeaKz}2B\x95|:\xc0b\xa0\x0b\x07\x9dNh"\xf7\xa9f\x98\x8a\xf9\\3(\x0f\xdf\xbc\x1b\x82mm\x8a\xc5\xf9g\x91\xa4\xcc\xc3^\xbb\x8c\xa7h\xcb\x00\xf8\x8cV\x07\x1a\xcfg\xff\xfen?M\xe5@DV\xc0]\xf4a\x80\n+\xb2*\xee\x1d2\xc6\xa9M\x10\x86A\xe0\x851\xf1 @ \xf2\xd4\xdfP\x01Y\xa1Q1dn\xcf\x82V\x1a\xd86\xb1\xe0b \x0c\xef\xb5\x90\x89\x85\xb3\x0c\nm\x00.\x9b6j\xe09\x08\x1e!\x94\xc2\xe4P\x18|Z\x84l\xee\x0c\xb4\xe5m\xb8\xb7\xb9\x83?4M(\x03\x9a\x16\xf2\x8b\x95\x15\x0f\x80\xc7\x03\t\xdc\x9e\x94Y\xf4\x18X9\xa9\xb8\xd8\xb3\xbf\xd4\xd3\x12f;\x81q\xd0\x00+Y6\x9aa\x0c\xe6\xce\x18\xd2\xdf>\xee\x01\x8e{\x8dEk\xecHt\x8d\xab\xbb\x19\x91\xfa\x1aT\xb4\xf871\xbc\x1b\x95~\xd5|\xc3\xb8\x84oG\xf2\xe2\x93b,\xdf\xae\x89MgzL\xcb\xfbb\xae\x85./\x00\x06i\xd3\x16\xf7\x85\xab\ru\xb7\xa6x{n\xc6\x8c\x91g\x1c\x9f\xee8E\x02\xdb\x9fd\xc6q\x15k@^\xe9\r"\x05q\xbfqa\xc6r\'\xd5\xa5\xbdyjx\xacG\xde8\x9e\xde\x9ah\xc4\x01\xbe\xdf\x94\xe1\x00\x05\xe9+\x00P\xb5w\x9d|\xcbcG\x8c\xd9\xdd3\x11\x1fh)\x95\xf2\xfe\xfeZAw\xf1\xff\xdb\xd1\xd6\x90\x8f\xf2\xbaCz]*)\xb7\xffv\xc9\xdb\xben\xb7\xfb%D\tN\x04CW+/7z\xe7\x04Q\x00r\xb7G\x9c\xb4\xa1`\x97\x8ddo\x9bv\x89+\xeaHx>le\x95\xde\xe3\xbb\x11=\x1a2\xc5\xd8\xcb\x01\x11\xaf\xac\xa9\x8b\xcbf\xa5\x8dR\t\xad5\x17\xf9\xfb4Z\xfe\xf6G\xff&4\r\xfe\x03\xa0\x88\xe3(\xff\xa1s\xf0\\\xac\xf4\x91\xe0\xc9\x8f|\x9e\x1c`+\xe5\xb8/\x18:\xad[f\x88\x94\xd9o\xcfa\xb6\x96\xcf\x0b%\x89i\x167bv\x18\x7fa\x18\nJ\xf6\x87\x97\xfb\x9dX.\x919T)lR<\xbcTf1\x00)\x99A\x95\'r\xed\xd6\xdb;\xb7\x06/\x1b\xcf\x9b\xcfD\x10!\xec\xa2\xa5@s:@C>\xc0v\xeb\xf7\xbcF\xcb\xb3\x85<5\'\xf2\xf0\xce\xcc\xf1\x82\xe0\xc5~\x88\xf8\xc2\x86ff\xc8\x13\xb4\x87\x98\xdf\xb18\x00\x0c\xc4\x97\xe52\xd7)n\xcb*\x9f\x97dP\x1c\xd8<\t\xd0\xa8V\xa6{6\xbfr?H\xa9\x8e\x99\xa2\xff\xbc\x81\x8bP7\x9e\x8b\xa7\x98]L\xbaM\xd2\x83*\xdf!Z\xaf0\xa8\xff_\x0f\xb8\xcc`l\xbaQ\x00\x12\xfd\x1aQ\xbe#t\x14\x1cF\xa0k\xdc\x08\x9b0\xe1>\x14\xf6\xc2.\xd8jp\xa6\xf4\xe7\xc9.o\xd1\x02\x1d\xd9\n\x1f\xaa\x9b\xc00_zF\x8f\xac\xbb\xe9\x9b`\x8c\xdd\xcb\xb0[=\x07<I\x97\xfd\x08\xb7l\x00\x11\x90\x16\x9a}\xa5\x00\xb3 L,\x98\xcc\xbb\xc1\xb9\xdbh5\r3\x12\xf5\x0f\xba6%\x04\x8f\xec)V\x82\xad\x9d\xdd\x01\x9a.\x8b`,\xdbL\x1aM\xf5\x86a49\xf7\xc2\x91\xa67$\xad-s "\xdcg\x001S\xb3\xd4\xa0*\x9e\x82\x1c|\x15c\x99\xcc\x97\xaa_\xfbD5b\x80&88\xa1;`\xe3\xddF\xf1\x06G\x89\xf7\xf8\xf5-\xcc\x14\xcfT\xd9\xb1q\xec\x96\x0b2\x88\xa8\x9d\xfd\xf5[\xf8W@A\x8a\x97\xad\xd8\x00\njk\x99)XF\xc5\xfai\x1d\xa7\rh\x80\xe6=$} \x95\xb6\x08\xa5"c\xe2\xd5\x97\x10\xa4l\xdfv\x8e\xa5\x881\xbd\x8e\n\x1d\xd36\xd7\x80\xd7}%\xa2\xa4Nd\xf7\xb5\xd6s\xf5lL\xd8D\xe4o\x01~[u\x1f\x81\x7f\x0c)\x05\xe6\xfd\xe5\xd14\\a\n\xc6I\xccJ\x0cXk\xcf,Z\x1c\xdb>\xe0\xc3\x10\xcehG\x89<\x0b\x08)\xd1\xe8\x99z9\xed\x08YJ6\x185\xd1\xbf9e&4\xb0\x18\xb7\x93\xfb\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00]e\xe8\xd1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00~[u\x1f\x81\x7f\x0c)\x05\xe6\xfd\xe5\xd14\\a\n\xc6I\xccJ\x0cXk\xcf,Z\x1c\xdb>\xe0\xc3z!\xc9N\xd5\x03\x8b^\xd9\xe6\xc7I\xba\xb1\x0fm\xd4\xa0=\xb6^s\x94_f\xb5\xc1\\n\xfe\xf9\xd2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\xd0\xe6k\xb8<N8W\xc3s$\x99\x9a+\xcc=o\x91\x18\x07\xbf\x8c\x926l\x14\xd2n<c\x9co\x83ZM\x81\xc4\x0f\xfcJVD\xdeZ\xf43\x18\x01|\xda\x88x!\xd2\xba\xd7\xa1\x9d\xd2\xf32\x8d" \x08\xee\x94ph\xaa4r\x97\'\x7fA<\xad\xd0\xce\xfa\xbdB\xc4R\xdd*,\x08\xd4\t\xd0\x97\x0f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n+\x93\xa0\x02\xe4\xc2\x1d\xaa5R\xe5,\xbd\xa5\x15|%}\xa4@\xe5\x11\x00\x80\x1fG\x8aH\x0b\xe7\xe9\x10\xd3tK\xda`\xb5u\xca\x8c\xa2\xf7n\x1d\xd5\x92l\xb13k\xdb\n+\xbe/\x1e\xc0\xfe\xbf\xd9\x83\x88V\x11]~.<\x14\x0f\xce`\x8b\xbf\xb9\xa7\xce"6\x19\xa5\x19|\x81!r\x15V\xa6\x82\x07\x96w\x98F\xce\xb2(G\xcfm\x17@t\xb2\x1b\xba\xcf4I}\x0b\xc4\n\xd4\x9b\xe2E\x9e\x84\x98mY||\xa8[+\x93\xa0\x02\xe4\xc2\x1d\xaa5R\xe5,\xbd\xa5\x15|%}\xa4@\xe5\x11\x00\x80\x1fG\x8aH\x0b\xe7\xe9\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # noqa: E501


def create_genesis_block(challenge_hash=bytes([0]*32)) -> FullBlock:
    plot_seed: bytes32 = ProofOfSpace.calculate_plot_seed(pool_pk, plot_pk)
    filename: str = "genesis-plot-" + token_hex(10)

    plotter = DiskPlotter()
    try:
        plotter.create_plot_disk(filename, k, b"genesis", plot_seed)

        prover = DiskProver(filename)

        qualities = prover.get_qualities_for_challenge(challenge_hash)

        if len(qualities) == 0:
            os.remove(filename)
            raise RuntimeError("No proofs for this challenge")

        proof_xs: bytes = prover.get_full_proof(challenge_hash, 0)
        proof_of_space: ProofOfSpace = ProofOfSpace(pool_pk, plot_pk, k, list(proof_xs))
    except KeyboardInterrupt:
        os.remove(filename)
        sys.exit(1)

    os.remove(filename)

    number_iters: uint64 = pot_iterations.calculate_iterations(proof_of_space, challenge_hash,
                                                               uint64(constants.DIFFICULTY_STARTING))

    disc: int = create_discriminant(challenge_hash, constants.DISCRIMINANT_SIZE_BITS)
    start_x: ClassGroup = ClassGroup.from_ab_discriminant(2, 1, disc)

    y_cl, proof_bytes = create_proof_of_time_nwesolowski(
        disc, start_x, number_iters, constants.DISCRIMINANT_SIZE_BITS, n_wesolowski)

    output = ProofOfTimeOutput(challenge_hash, number_iters,
                               ClassgroupElement(y_cl[0], y_cl[1]))

    proof_of_time = ProofOfTime(output, n_wesolowski, [uint8(b) for b in proof_bytes])

    coinbase: CoinbaseInfo = CoinbaseInfo(0, block_rewards.calculate_block_reward(uint32(0)),
                                          coinbase_target)
    coinbase_sig: PrependSignature = sk.sign_prepend(coinbase.serialize())
    fees_target: FeesTarget = FeesTarget(fee_target, 0)

    body: BlockBody = BlockBody(coinbase, coinbase_sig, fees_target, None, bytes([0]*32))

    timestamp = uint64(time.time())

    header_data: BlockHeaderData = BlockHeaderData(bytes([0]*32), timestamp, bytes([0]*32),
                                                   proof_of_space.get_hash(), body.get_hash(),
                                                   bytes([0]*32))

    header_sig: PrependSignature = sk.sign_prepend(header_data.serialize())
    header: BlockHeader = BlockHeader(header_data, header_sig)

    challenge = Challenge(proof_of_space.get_hash(), proof_of_time.get_hash(), 0,
                          uint64(constants.DIFFICULTY_STARTING), 0)
    trunk_block = TrunkBlock(proof_of_space, proof_of_time, challenge, header)

    full_block: FullBlock = FullBlock(trunk_block, body)

    return full_block


# block = create_genesis_block()
# print(block.serialize())
