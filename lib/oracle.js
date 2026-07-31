import oracledb from "oracledb";

oracledb.outFormat = oracledb.OUT_FORMAT_OBJECT;

let pool;

export async function getConnection() {
  try {
    if (!pool) {
      pool = await oracledb.createPool({
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        connectString: process.env.DB_CONNECT_STRING,
        poolMin: 1,
        poolMax: 5,
        poolIncrement: 1,
      });
    }

    return await pool.getConnection();
  } catch (err) {
    console.error("Oracle Error:", err);
    throw err;
  }
}