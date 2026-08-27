import { NextResponse } from "next/server";
import { getConnection } from "@/lib/oracle";

export async function POST(request) {
  let connection;

  try {
    const { email, password } = await request.json();

    connection = await getConnection();

    const result = await connection.execute(
      `SELECT
          user_id,
          name,
          email
       FROM users
       WHERE email = :email
       AND password = :password`,
      {
        email,
        password,
      }
    );

    if (result.rows.length === 0) {
      return NextResponse.json({
        success: false,
        message: "Invalid email or password",
      });
    }

    return NextResponse.json({
      success: true,
      message: "Login successful",
      user: result.rows[0],
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