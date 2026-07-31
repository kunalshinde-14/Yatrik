import { NextResponse } from "next/server";
import { getConnection } from "@/lib/oracle";

export async function GET() {
  let connection;

  try {
    connection = await getConnection();

    const result = await connection.execute(
      `SELECT train_name FROM trains ORDER BY train_id`
    );

    return NextResponse.json({
      success: true,
      trains: result.rows,
    });

  } catch (error) {

    console.error(error);

    return NextResponse.json({
      success: false,
      message: error.message,
    });

  } finally {

    if (connection) {
      await connection.close();
    }
  }
}