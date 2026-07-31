import oracledb from "oracledb";

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
  } catch (error) {
    console.error("Oracle Connection Error:", error);
    throw error;
  }
}