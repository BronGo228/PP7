using System.Data.SqlClient;

namespace SmartphoneDefects
{
    public static class Db
    {
        public static string ConnectionString =
            @"Server=localhost;Database=SmartphoneDefectsDB;Trusted_Connection=True;";

        public static SqlConnection GetConnection()
        {
            return new SqlConnection(ConnectionString);
        }
    }
}
