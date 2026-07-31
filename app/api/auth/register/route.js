import { NextResponse } from "next/server";
import { getConnection } from "@/lib/oracle";

export async function POST(request) {
  let connection;

  try {
    const { name, email, phone, password } = await request.json();

    connection = await getConnection();

    // Check if email already exists
    const existingUser = await connection.execute(
      `SELECT user_id
       FROM users
       WHERE email = :email`,
      { email }
    );

    if (existingUser.rows.length > 0) {
      return NextResponse.json({
        success: false,
        message: "Email already registered",
      });
    }

    // Insert new user
    await connection.execute(
      `INSERT INTO users
       (name, email, phone, password)
       VALUES
       (:name, :email, :phone, :password)`,
      {
        name,
        email,
        phone,
        password,
      },
      {
        autoCommit: true,
      }
    );

    return NextResponse.json({
      success: true,
      message: "Registration successful",
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