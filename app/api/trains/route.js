import { NextResponse } from "next/server";
import { getConnection } from "@/lib/oracle";

export async function GET(request) {
  let connection;

  try {
    const { searchParams } = new URL(request.url);

    const source = searchParams.get("source");
    const destination = searchParams.get("destination");

    connection = await getConnection();

    let query = `
      SELECT
        train_id,
        train_number,
        train_name,
        source,
        destination,
        fare
      FROM trains
    `;

    const binds = {};

    // Search by both stations
    if (source && destination) {
      query += `
        WHERE LOWER(source) = LOWER(:source)
        AND LOWER(destination) = LOWER(:destination)
      `;

      binds.source = source;
      binds.destination = destination;
    }

    // Search only by source
    else if (source) {
      query += `
        WHERE LOWER(source) = LOWER(:source)
      `;

      binds.source = source;
    }

    // Search only by destination
    else if (destination) {
      query += `
        WHERE LOWER(destination) = LOWER(:destination)
      `;

      binds.destination = destination;
    }

    query += `
      ORDER BY train_name
    `;

    const result = await connection.execute(query, binds);

    return NextResponse.json({
      success: true,
      data: result.rows,
    });

  } catch (error) {
    console.error("Train Search Error:", error);

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