from difflib import get_close_matches
import ogr
import os
import sys

import numpy as np
import redis

class Halimun:
    """
    Mencari administrasi geolevel in Indonesia
    """
    def __init__(self, server):
        self.rc = redis.StrictRedis(host=server, port=6379, db=0)
        # make sure all data exists in mercached
        self.daftar_provinsi = self.rc.hkeys("daftar-provinsi")
        self.daftar_kabupaten = self.rc.hkeys("daftar-kabupaten")
        self.daftar_kecamatan = self.rc.hkeys("daftar-kecamatan")
        self.daftar_kelurahan = self.rc.hkeys("daftar-kelurahan")
        self.daftar_geolevel = {
                "provinsi": self.daftar_provinsi,
                "kabupaten": self.daftar_kabupaten,
                "kecamatan": self.daftar_kecamatan,
                "kelurahan": self.daftar_kelurahan,
                }
        self.daftar_id_kelurahan = self.rc.get("daftar-id-kelurahan")
        self.daftar_id_kelurahan_num = np.array(
                self.daftar_id_kelurahan.split(","), dtype=np.int64)

    def cari_admin(self, query, geolevel):
        """
        query: admin yang hendak kau cari
        geolevel: level admin, salah satu dari (lowercase)
            - provinsi
            - kabupaten
            - kecamatan
            - kelurahan
        """
        query_norm = query.lower()
        key_geolevel = "daftar-%s" %(geolevel.lower())
        id_admin = self.rc.hget(key_geolevel, query_norm)
        if id_admin:
            return int(id_admin)
        else:
            try:
                key_approx = get_close_matches(
                        query_norm,
                        self.daftar_geolevel[geolevel.lower()])[0]
                id_admin = self.rc.hget(key_geolevel, key_approx)
                return int(id_admin)
            except IndexError:
                raise RuntimeError("Info admin %s %s not found" %(geolevel, query))

    def pilih_banyak_provinsi_dari_cresta(self, cresta, quantity):
        """
        expected return:
        two list:
        - id_admin
        - quantity distribution for each ida_admin
        """
        n_init = 5
        init_provinsi = np.zeros(n_init)
        for i in xrange(n_init):
            init_provinsi[i] = self.cari_provinsi_dari_cresta(cresta)
        uniq_provinsi = np.unique(init_provinsi)
        n_provinsi = np.alen(uniq_provinsi)
        val_quan = quantity / np.int(n_provinsi)
        uniq_quantity = np.zeros(n_provinsi)
        for i in xrange(n_provinsi-1):
            uniq_quantity[i] = val_quan
        uniq_quantity[-1] = quantity - np.sum(uniq_quantity)
        assert np.sum(uniq_quantity) == quantity
        return (uniq_provinsi, uniq_quantity)

    def cari_provinsi_dari_cresta(self, id_cresta):
        """
        sebuah cresta dapat terdiri dari banyak provinsi
        """
        try:
            keys_set = "mapping-cresta-%s-provinsi" %(int(float((id_cresta))))
        except ValueError:
            raise RuntimeError("Input cresta using numerical value, please.")
        id_provinsi = self.rc.srandmember(keys_set)
        return int(id_provinsi)

    def cari_cresta_dari_provinsi(self, id_provinsi):
        keys_hash = "mapping-provinsi-cresta"
        keys_provinsi = "provinsi-%d" %(int(id_provinsi))
        id_cresta = self.rc.hget(keys_hash, keys_provinsi)
        return int(id_provinsi)

    def pilih_banyak_kecamatan_dari_kodepos(self, kodepos, quantity):
        n_init = 5
        init_kecamatan = np.zeros(n_init)
        for i in xrange(n_init):
            init_kecamatan[i] = self.cari_kecamatan_dari_kodepos(kodepos)
        uniq_kecamatan = np.unique(init_kecamatan)
        n_kecamatan = np.alen(uniq_kecamatan)
        val_quan = quantity / np.int(n_kecamatan)
        uniq_quantity = np.zeros(n_kecamatan)
        for i in xrange(n_kecamatan-1):
            uniq_quantity[i] = val_quan
        uniq_quantity[-1] = quantity - np.sum(uniq_quantity)
        assert np.sum(uniq_quantity) == quantity
        return (uniq_kecamatan, uniq_quantity)

    def cari_kecamatan_dari_kodepos(self, kodepos):
        """
        sebuah kodepos dapat terdiri dari banyak kecamatan
        """
        print kodepos
        try:
            num_kodepos = int(float(kodepos))
        except ValueError:
            num_kodepos = self._hitung_kodepos_digit(kodepos)
        keys_set = "mapping-kodepos-%d-kecamatan" %(num_kodepos)
        id_kecamatan = self.rc.srandmember(keys_set)
        return int(id_kecamatan)

    def _hitung_kodepos_digit(self, kodepos):
        """
        Kodepos di Indonesia umumnya terdiri dari lima digit angka,
        namun ada softaware tertentu yang menambahkan huruf dibelakang kodepos
        tersebut.

        Fungsi ini mengambil 4 digit paling depan kodepos
        """
        emp_kodepos = str(kodepos)[:4]
        try:
            num_kodepos = int(float(emp_kodepos))
            return num_kodepos
        except ValueError:
            raise RuntimeError("Bukan format kodepos yang benar")

    def pilih_banyak_desa(self, geoname, geolevel, quantity):
        """
        pilih desa
        """
        # 10 pangkat (jumlah digit relatif terhadap jumlah id digit kelurahan)
        geolevel_divisor = {
                "provinsi": np.int(1e8),
                "kabupaten": np.int(1e6),
                "kecamatan": np.int(1e3),
                "kelurahan": np.int(1e0),
                }

        # validasi tipe geolevel
        if geolevel in ("cresta", "provinsi", "kabupaten", "kodepos",
                "kecamatan", "kelurahan"):
            pass
        else:
            raise RuntimeError("Level administrasi tidak dikenali")

        if geolevel == "cresta":
            div_factor = geolevel_divisor["provinsi"]
            pilihan_provinsi = self.pilih_banyak_provinsi_dari_cresta(geoname, quantity)
            daftar_id_admin = pilihan_provinsi[0]
            dist_quantity = pilihan_provinsi[1]
        elif geolevel == "kodepos":
            div_factor = geolevel_divisor["kecamatan"]
            pilihan_kecamatan = self.pilih_banyak_kecamatan_dari_kodepos(geoname, quantity)
            daftar_id_admin = pilihan_kecamatan[0]
            dist_quantity = pilihan_kecamatan[1]
        else:
            id_admin = self.cari_admin(geoname, geolevel)
            div_factor = geolevel_divisor[geolevel]
            daftar_id_admin = np.array([id_admin], dtype=np.int)
            dist_quantity = np.array([quantity], dtype=np.int)

        div_id_kelurahan = self.daftar_id_kelurahan_num / div_factor

        temp_hasil = []
        for i,j in zip(daftar_id_admin, dist_quantity):
            ind_id_kelurahan = np.nonzero(div_id_kelurahan==i)[0]
            fil_id_kelurahan = self.daftar_id_kelurahan_num[ind_id_kelurahan]
            sam_id_kelurahan = np.random.choice(fil_id_kelurahan, size=np.int(j))
            temp_hasil.append(sam_id_kelurahan)
        final_hasil = np.hstack(np.array(temp_hasil))
        return (geolevel, geoname, final_hasil)

    def hitung_random_point(self, id_desa):
        """
        geometry_desa: dapet dari redis, bentuk string wkt
        """
        #TODO: hitung random point 
        key_hash = "geom-kelurahan-wkt"
        kelurahan_wkt = self.rc.hget(key_hash, id_desa)
        geom = ogr.CreateGeometryFromWkt(str(kelurahan_wkt)) 
        envelope = geom.GetEnvelope()
        while True:
            #x is random longitude, y is random latitude
            x = np.random.uniform(low=envelope[0], high=envelope[1])
            y = np.random.uniform(low=envelope[2], high=envelope[3])
            wkt = "POINT (%s %s)" %(x,y)
            point = ogr.CreateGeometryFromWkt(wkt)
            if geom.Contains(point):
                return (x,y)

