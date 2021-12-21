"""Unittests for main.py"""
from unittest.mock import patch, call

import unittest

import main, bobcat, checks


class TestMain(unittest.TestCase):
    def setUp(self):
        self.mock_status = {
            "status": "Synced",
            "gap": "0",
            "miner_height": "1148539",
            "blockchain_height": "1148539",
            "epoch": "30157",
        }

        self.mock_miner = {
            "ota_version": "1.0.2.66",
            "region": "region_us915",
            "frequency_plan": "us915",
            "animal": "my-mocked-miner",
            "pubkey": "112YUf4TUQy4bxXRvGjrj6z7XyiSx8FDudTn6vtRYPgoGPnjBGWW",
            "miner": {
                "State": "running",
                "Status": "Up 36 hours",
                "Names": ["/miner"],
                "Image": "quay.io/team-helium/miner:miner-arm64_2021.12.14.0_GA",
                "Created": 1639980913,
            },
            "p2p_status": [
                "+---------+-------+",
                "|  name   |result |",
                "+---------+-------+",
                "|connected|  yes  |",
                "|dialable |  yes  |",
                "|nat_type | none  |",
                "| height  |1148539|",
                "+---------+-------+",
                "",
                "",
            ],
            "miner_height": "1148539",
            "epoch": "30157",
            "ports_desc": "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
            "ports": {
                "192.168.0.8:22": "open",
                "192.168.0.8:44158": "open",
                "33.117.96.28:22": "closed/timeout",
                "33.117.96.28:44158": "closed/timeout",
            },
            "private_ip": "192.168.0.8",
            "public_ip": "33.117.96.28",
            "peerbook": [
                "+-----------------------------------------------+--------------+----------+---------+---+----------+",
                "|                    address                    |     name     |listen_add|connectio|nat|last_updat|",
                "+-----------------------------------------------+--------------+----------+---------+---+----------+",
                "|/p2p/332YUS4TUQy4boXRvGjrj6z7XyiSx8FDxmTn6vtRYP|my-mock-miner |    1     |    7    |non| 293.353s |",
                "+-----------------------------------------------+--------------+----------+---------+---+----------+",
                "",
                "+---------------------------+",
                "|listen_addrs (prioritized) |",
                "+---------------------------+",
                "|/ip4/33.117.96.28/tcp/44158|",
                "+---------------------------+",
                "",
                "+------------------+---------------------+----------------------------------------+----------------+",
                "|      local       |       remote        |                  p2p                   |      name      |",
                "+------------------+---------------------+----------------------------------------+----------------+",
                "|/ip4/172.17.0.2/tc|/ip4/33.223.200.123/t|/p2p/2228k7YK3Ufah5qaAp37qe2jw3LaG6ycQUA|mock-peer-1     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.150.110.17/tc|/p2p/332qFc4yctCWyZyFaDhs4ve2ZsNEn1CKS1G|mock-peer-2     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.12.228.218/tc|/p2p/338eczMRVEBBeoCxiYjaZssdcHQXVk9Zokq|mock-peer-3     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.0.245.53/tcp/|/p2p/33Uyz1JBMcatg4SVYRRk2cxTz3tzvaKcFR7|mock-peer-4     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.37.13.24/tcp/|/p2p/33afuQSrmka2mgxLu91AdtDXbJ9wmqWBUxC|mock-peer-5     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.197.157.248/t|/p2p/33i6EevWXa6cskJepj8UnwMaKkPabZgK6QN|mock-peer-6     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.230.47.214/tc|/p2p/33sogMFP3m6Vgh2hsb3YCaRmG4GpyHdA1HH|mock-peer-7     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.68.166.175/tc|/p2p/33vTBsa1iXjy7QmFs6HFTSqK8ckSejQ3nwZ|mock-peer-8     |",
                "|/ip4/172.17.0.2/tc|/ip4/33.238.156.97/tc|/p2p/33w77YQLhgUt8HUJrMtntGGrs7RyXmot1of|mock-peer-9     |",
                "+------------------+---------------------+----------------------------------------+----------------+",
                "",
                "",
            ],
            "height": ["30157    1148539", ""],
            "temp0": "38 °C",
            "temp1": "37 °C",
            "timestamp": "2021-12-21 18:18:39 +0000 UTC",
            "errors": "",
        }

        self.mock_speed = {
            "DownloadSpeed": "94 Mbit/s",
            "UploadSpeed": "57 Mbit/s",
            "Latency": "7.669083ms",
        }

    def test_check_is_healthy(self):
        """Test check is healthy"""
        result = checks.is_healthy(self.mock_status, self.mock_miner)
        self.assertEqual(result, True)

    def test_check_is_relayed(self):
        """Test check is relayed"""
        result = checks.is_relayed(self.mock_miner)
        self.assertEqual(result, False)

    def test_check_has_errors(self):
        """Test check has errors"""
        result = checks.has_errors(self.mock_miner)
        self.assertEqual(result, False)

    def test_check_should_fastsync(self):
        """Test check should fastsync"""
        result = checks.should_fastsync(self.mock_status)
        self.assertEqual(result, False)

    def test_check_should_resync(self):
        """Test check should resync"""
        result = checks.should_fastsync(self.mock_status)
        self.assertEqual(result, False)

    def test_check_should_reset(self):
        """Test check should reset"""
        result = checks.should_fastsync(self.mock_status)
        self.assertEqual(result, False)


if __name__ == "__main__":
    unittest.main()